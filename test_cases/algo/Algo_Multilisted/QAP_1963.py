import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from datetime import datetime, timedelta
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from stubs import Stubs
from test_framework.data_sets import constants


class QAP_1963(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region order parameters
        self.qty = 2000
        self.stop_price = 40
        self.order_type_stop = 3
        self.order_type_mkt = 1
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value

        now = datetime.today() - timedelta(hours=3)
        self.ExpireDate = (now + timedelta(days=1)).strftime("%Y%m%d")
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_5")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_2")
        self.s_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        market_rule = rule_manager.add_NewOrdSingle_Market(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, 0)
        self.rule_list = [ocr_rule,market_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_0 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_0)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, OrdType=self.order_type_stop, TimeInForce=self.tif_gtd, ExpireDate=self.ExpireDate, Instrument=self.instrument, StopPx=self.stop_price))
        self.multilisting_order.remove_parameter('Price')

        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_0)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod,message_name='Sell side NewOrderSingle')

        pending_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        pending_multilisting_order_params.add_tag(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_sell.check_fix_message(pending_multilisting_order_params, key_parameters=self.key_params_cl,message_name='Sell side ExecReport PendingNew')

        new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        new_multilisting_order_params.add_tag(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_sell.check_fix_message(new_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Send MD
        case_id_1 = bca.create_event("Send Market Data", self.test_id)

        MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol="734",
            connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
        )).MDRefID

        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }

        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_1,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
        ))
        time.sleep(10)
        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }

        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_1,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
        ))

        time.sleep(2)

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA 1 order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(OrderQty=self.qty, OrdType=self.order_type_mkt, TimeInForce=self.tif_gtd, ExpireDate=self.ExpireDate, Instrument=self.instrument))
        self.dma_1_order.remove_parameter('Price')
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params,message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order,self.gateway_side_buy, self.status_pending)
        pending_dma_1_order_params.add_tag(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params,direction=self.ToQuod,message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order,self.gateway_side_buy, self.status_pending)
        new_dma_1_order_params.add_tag(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params,direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region check Eliminate
        case_id_3 = bca.create_event("Eliminate Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        # region Check child Eliminate
        eliminate_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy,self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(eliminate_dma_1_order, self.key_params, self.ToQuod, "Buy side ExecReport Eliminate child order")
        # endregion

        # region check parent Eliminate
        eliminate_multilisting_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(eliminate_multilisting_order, key_parameters=self.key_params, message_name="Sell side ExecReport Eliminate")
        # endregion
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager.remove_rules(self.rule_list)
