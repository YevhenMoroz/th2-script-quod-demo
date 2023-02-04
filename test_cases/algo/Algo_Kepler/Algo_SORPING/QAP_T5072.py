import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T5072(TestCase):
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
        self.qty = 1500
        self.price = 20
        self.inc_price = 35
        self.traded_qty = 500
        self.leaves_after_amend = self.qty - self.traded_qty
        self.qty_bid = 1000
        self.qty_ask = 100
        self.price_ask = 40
        self.price_bid = 30
        self.new_ask_price_qdl2 = 35
        self.new_ask_qty_qdl2 = 500
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.tif_iok = constants.TimeInForce.ImmediateOrCancel.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_partial_fill = Status.PartialFill
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_8")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit1 = self.data_set.get_mic_by_name("mic_10")
        self.ex_destination_quodlit2 = self.data_set.get_mic_by_name("mic_11")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_fill_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_Reject_Eliminate_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.inc_price)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit2, True, self.traded_qty, self.inc_price)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_ioc_rule, ocrr_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion


        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_1_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message(self.dma_1_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_new)
        er_new_dma_1_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Modify parent SORPING order
        case_id_2 = bca.create_event("Replace MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.SORPING_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.SORPING_order)
        self.SORPING_order_replace_params.change_parameters(dict(Price=self.inc_price))
        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order_replace_params, case_id_2)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.SORPING_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replaced_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        time.sleep(3)

        # region check cancel first dma child order
        er_cancel_dma_1_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_1_qdl1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("New child DMA order", self.test_id))

        self.dma_2_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.qty, Price=self.inc_price))
        self.fix_verifier_buy.check_fix_message(self.dma_2_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_new)
        er_new_dma_2_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Update_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.new_ask_price_qdl2, MDEntrySize=self.new_ask_qty_qdl2)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.new_ask_qty_qdl2)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)
        # endregion

        # region Check amend second child order
        replaced_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_cancel_replace)
        replaced_dma_order_params.change_parameters(dict(OrderQty=self.leaves_after_amend))
        self.fix_verifier_buy.check_fix_message(replaced_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy Side ExecReport Replace Request')
        # endregion

        # region Check aggressive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Aggressive child DMA order", self.test_id))

        self.dma_qdl2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qdl2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit2, OrderQty=self.traded_qty, Price=self.inc_price, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_qdl2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 3 order')

        er_pending_new_dma_qdl2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_qdl2_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit2))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_qdl2_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        er_new_dma_qdl2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_new)
        er_new_dma_qdl2_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit2))
        self.fix_verifier_buy.check_fix_message(er_new_dma_qdl2_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion

        # region Check Fill
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill aggressive child Order", self.test_id))
        # Fill Order
        fill_dma_qdl2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_fill)
        fill_dma_qdl2_order.change_parameters(dict(CumQty=self.traded_qty, LeavesQty=0, LastQty=self.traded_qty, LastPx=self.inc_price))
        self.fix_verifier_buy.check_fix_message(fill_dma_qdl2_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill')

        self.fix_verifier_sell.set_case_id(bca.create_event("Partial fill Algo Order", self.test_id))
        partially_fill_SORPING_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_partial_fill)
        partially_fill_SORPING_order.change_parameters(dict(Price=self.inc_price, LastPx=self.inc_price, CumQty=self.traded_qty, LeavesQty=self.leaves_after_amend, LastQty=self.traded_qty)).add_tag(dict(SettlType="*"))
        self.fix_verifier_sell.check_fix_message(partially_fill_SORPING_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partially Fill')
        # endregion

        time.sleep(15)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel third dma child order
        er_cancel_dma_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_qdl1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 2 order")
        # endregion

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
