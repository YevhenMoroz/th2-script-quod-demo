import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager


class QAP_T8748(TestCase):
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
        self.order_type = constants.OrderType.Limit.value
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value

        self.price_ask = 10_000
        self.qty_ask = 130.5

        self.price_bid = 130.05
        self.qty_bid = 10_000

        self.price_ltq = 130.2
        self.qty_ltq = 10_000

        self.qty = 500_000
        self.price = 135
        
        self.price_vwap_child = 130         #PRM - 1bps
        self.executed_would_qty = 10_000

        self.custom_value = constants.Custom.Passive.value
        self.would_price_reference = constants.Reference.Primary.value
        self.would_price_offset = 20
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        self.status_cancel = Status.Cancel
        self.status_eliminated = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_36")
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_vwap_child)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.executed_would_qty, self.price_ask)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_ioc_rule, ocr_rule]
        # endregion

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to trigger the WouldPrice behavior", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the WouldPrice behavior", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create VWAP Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.vwap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_VWAP_Redburn_params()
        self.vwap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.vwap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.vwap_order.update_fields_in_component('QuodFlatParameters', dict(Custom=self.custom_value, WouldPriceReference=self.would_price_reference, WouldPriceOffset=self.would_price_offset))
        self.fix_manager_sell.send_message_and_receive_response(self.vwap_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_vwap_parent = self.vwap_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_vwap_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_vwap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_vwap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_vwap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_vwap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check IOC child order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("VWAP DMA child order", self.test_id))

        dma_child_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_child_order_1.change_parameters(dict(OrderQty='%\d+', Price=self.price_vwap_child, Instrument='*', TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(dma_child_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle VWAP DMA child order')

        pending_dma_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_child_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew VWAP DMA child order')

        new_dma_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_child_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New VWAP DMA child order')
        # endregion
        #
        # # region Clear Market Data
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to update the BestAsk", self.test_id))
        # market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask_1)
        # self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        #
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the WorsePrice behavior", self.test_id))
        # market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        # market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_2)
        # self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        #
        # time.sleep(3)
        # # endregion
        #
        # # region Check IOC child order 2
        # self.fix_verifier_buy.set_case_id(bca.create_event("IOC child order - 2", self.test_id))
        #
        # ioc_child_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        # ioc_child_order_2.change_parameters(dict(OrderQty=self.qty_ask_1, Price=self.price_ask_2, Instrument='*', TimeInForce=self.tif_ioc))
        # self.fix_verifier_buy.check_fix_message(ioc_child_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle IOC Child 2')
        #
        # pending_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  IOC Child 2')
        #
        # new_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(new_ioc_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  IOC Child 2')
        #
        # cancel_ioc_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_eliminated)
        # cancel_ioc_child_order_2.change_parameters(dict(OrdType=self.order_type, TimeInForce=self.tif_ioc))
        # self.fix_verifier_buy.check_fix_message(cancel_ioc_child_order_2, self.key_params, self.ToQuod, "Buy Side ExecReport Partial Fill IOC Child 2")
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_vwap_order = FixMessageOrderCancelRequest(self.vwap_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_vwap_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_vwap_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancellation parent POV order
        cancel_vwap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_vwap_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)