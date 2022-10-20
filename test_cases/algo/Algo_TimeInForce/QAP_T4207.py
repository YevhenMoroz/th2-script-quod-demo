import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_T4207(TestCase):
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
        self.qty = 3000000
        self.price = 20
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 10000
        self.delay = 3000
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value
        now = datetime.utcnow()
        self.ExpireDate = (now + timedelta(days=4)).strftime("%Y%m%d")
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.listing_id_par = self.data_set.get_listing_id_by_name("listing_1")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_eliminate_rule = rule_manager.add_NewOrderSingle_ExecutionReport_Eliminate(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price, self.delay)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_eliminate_rule, ocr_rule, nos_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for TIF order
        case_id_1 = bca.create_event("Create Synthetic TIF Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Synthetic_TIF_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TIF_params()
        self.Synthetic_TIF_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Synthetic_TIF_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate=self.ExpireDate))
        self.fix_manager_sell.send_message_and_receive_response(self.Synthetic_TIF_order, case_id_1)
        # endregion
        time.sleep(2)

        rule_manager.remove_rule(nos_eliminate_rule)

        # region Check Sell side
        self.fix_verifier_sell.set_case_id(bca.create_event("Check Synthetic TIF order", self.test_id))
        self.fix_verifier_sell.check_fix_message(self.Synthetic_TIF_order, self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_DMA(self.Synthetic_TIF_order, self.status_pending)
        er_pending_new_Synthetic_TIF_order_params.remove_parameter('NoParty').add_tag(dict(TargetStrategy='*')).change_parameter('ExpireDate', '*')
        self.fix_verifier_sell.check_fix_message(er_pending_new_Synthetic_TIF_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        er_new_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_DMA(self.Synthetic_TIF_order, self.status_new)
        er_new_Synthetic_TIF_order_params.add_tag(dict(TargetStrategy='*')).add_tag(dict(NoParty='*')).change_parameter('ExpireDate', '*')
        self.fix_verifier_sell.check_fix_message(er_new_Synthetic_TIF_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order 1", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty, Price=self.price, Instrument='*'))
        
        er_pending_new_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_order, self.key_params_cl, self.ToQuod, "Buy Side ExecReport Pending new child DMA order")

        er_new_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order, self.key_params_cl, self.ToQuod, message_name='Buy Side ExecReport New child DMA order')
        # endregion

        time.sleep(2)
        
        # region Check eliminate child DMA order
        er_eliminate_dma_order_params = FixMessageExecutionReportAlgo().set_params_for_nos_eliminate_rule(self.dma_order)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate Child DMA 1 order')
        # endregion

        # region Check child DMA order 2
        self.fix_verifier_buy_2 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        time.sleep(5)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Child DMA order 2", self.test_id))
        self.dma_order_2 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_params()
        self.dma_order_2.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty, Price=self.price, Instrument='*'))
        
        er_pending_new_dma_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy_2.check_fix_message(er_pending_new_dma_order_2, self.key_params_cl, self.ToQuod, "Buy Side ExecReport Pending new child DMA order")

        er_new_dma_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy_2.check_fix_message(er_new_dma_order_2, self.key_params_cl, self.ToQuod, message_name='Buy Side ExecReport New child DMA order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Synthetic TIF order
        case_id_2 = bca.create_event("Cancel Synthetic TIF Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Synthetic_TIF_order = FixMessageOrderCancelRequest(self.Synthetic_TIF_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Synthetic_TIF_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Synthetic_TIF_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # endregion

        # region Check that Synthetic TIF order was canceled
        er_cancel_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_DMA(self.Synthetic_TIF_order, self.status_cancel)
        er_cancel_Synthetic_TIF_order_params.change_parameters(dict(TargetStrategy='*', NoParty='*', ExpireDate='*'))
        self.fix_verifier_sell.check_fix_message(er_cancel_Synthetic_TIF_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion

        # time.sleep(5)

        #region Check cancel DMA order 2
        er_cancel_DMA_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy_2.check_fix_message(er_cancel_DMA_order_2_params, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Buy side Cancel Child DMA order 2')

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)