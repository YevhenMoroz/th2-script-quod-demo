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
from datetime import datetime
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from stubs import Stubs
from test_framework.data_sets import constants


class QAP_1985(TestCase):
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
        self.qty = 1300
        self.price = 35
        self.stop_price = 30
        self.order_type_stop_lmt = 4
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1000000
        self.tif_gtc = constants.TimeInForce.GoodTillCancel.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
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

        # region Send_MarketData
        case_id_0 = bca.create_event("Send Market Data", self.test_id)

        self.fix_manager_feed_handler.set_case_id(case_id_0)
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(case_id_0)
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID( self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, OrdType=self.order_type_stop_lmt, TimeInForce=self.tif_gtc, Instrument=self.instrument, StopPx=self.stop_price))

        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod,message_name='Sell side NewOrderSingle')

        pending_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        pending_multilisting_order_params.add_tag(dict(StopPx=self.stop_price))
        self.fix_verifier_sell.check_fix_message(pending_multilisting_order_params, key_parameters=self.key_params_cl,message_name='Sell side ExecReport PendingNew')

        new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        pending_multilisting_order_params.add_tag(dict(StopPx=self.stop_price))
        self.fix_verifier_sell.check_fix_message(new_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Send MarketData
        case_id_2 = bca.create_event("Send Market Data", self.test_id)

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
                    'MDEntryPx': '35',
                    'MDEntrySize': '2000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
        ))
        time.sleep(10)
        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '35',
                    'MDEntrySize': '2000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
        ))
        time.sleep(2)
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA 1 order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(OrderQty=self.qty, Price=self.price, TimeInForce=self.tif_gtc, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params,message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order,self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params,direction=self.ToQuod,message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order,self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params,direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_multilisting_order = FixMessageOrderCancelRequest(self.multilisting_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_multilisting_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        cancel_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")

        cancel_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single( self.multilisting_order, self.gateway_side_sell, self.status_cancel)
        cancel_multilisting_order_params.change_parameters(dict(TimeInForce=self.tif_gtc))
        self.fix_verifier_sell.check_fix_message(cancel_multilisting_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion

        RuleManager.remove_rules(self.rule_list)
