import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo


class QAP_T8790(TestCase):
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
        self.qty = 141
        self.price = 45
        self.traded_ioc_qty = 0
        self.aggressive_qty = 94
        self.passive_qty = 47
        self.qty_for_md_qdl8 = 94
        self.qty_for_md_qdl9 = 1000
        self.price_ask_qdl8 = 44
        self.price_bid = 30
        self.price_ask_qdl9 = 46
        self.price_ask_qdl10 = 46
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.delay_for_trade = 2000
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_9.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_15")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit8 = self.data_set.get_mic_by_name("mic_24")
        self.ex_destination_quodlit9 = self.data_set.get_mic_by_name("mic_25")
        self.ex_destination_quoddkp1 = self.data_set.get_mic_by_name("mic_14")
        self.ex_destination_quoddkp2 = self.data_set.get_mic_by_name("mic_15")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl8 = self.data_set.get_listing_id_by_name("listing_17")
        self.listing_id_qdl9 = self.data_set.get_listing_id_by_name("listing_18")
        self.listing_id_qdl10 = self.data_set.get_listing_id_by_name("listing_19")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        self.key_params_ER_cancel_reject_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        self.key_params_specific_cancel = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_with_text")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit8, False, self.traded_ioc_qty, self.price_ask_qdl8, 1000)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, self.price, self.price, self.passive_qty, self.passive_qty, self.delay_for_trade)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, False, 1000)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit8, self.price)
        self.ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit8, True)
        self.rule_list = [nos_ioc_rule, nos_1_rule, nos_trade_rule, ocrr_rule, nos_2_rule, ocr_2_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl8 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md_qdl8)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl8, MDEntrySize=self.qty_for_md_qdl8)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)

        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl9 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl9, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md_qdl9)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl9, MDEntrySize=self.qty_for_md_qdl9)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl9)

        market_data_snap_shot_qdl9 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl9, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl9)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl10 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl10, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl10.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md_qdl9)
        market_data_snap_shot_qdl10.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl10, MDEntrySize=self.qty_for_md_qdl9)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl10)

        market_data_snap_shot_qdl10 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl10, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl10.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl10)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl8 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md_qdl8)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl9, MDEntrySize=self.qty_for_md_qdl8)

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check aggressive DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA orders", self.test_id))

        self.dma_1_qdl8_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl8_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit8, OrderQty=self.aggressive_qty, Price=self.price_ask_qdl8, TimeInForce=self.tif_ioc, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_qdl8_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA order')

        er_eliminate_dma_1_qdl8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl8_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_dma_1_qdl8_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate Aggressive Child DMA order')
        # endregion

        # region Check the passive child on the MTF
        self.dma_1_qdl9_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl9_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit9, OrderQty=self.passive_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_qdl9_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 1 order on the MTF')

        er_pending_new_dma_1_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl9_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child DMA 1 order on the MTF')

        er_new_dma_1_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl9_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child DMA 1 order on the MTF')

        time.sleep(3)

        er_fill_dma_1_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl9_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_1_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Passive Child DMA 1 order on the MTF')
        # endregion

        time.sleep(3)

        # region Check reject replace child (recycling eliminated qty)
        er_reject_replaced_dma_1_qdl9_order_params = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.dma_1_qdl9_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_replaced_dma_1_qdl9_order_params, self.key_params_ER_cancel_reject_child, self.ToQuod, 'Buy Side OrderCancelRejectReport Child DMA 1 order on the MTF')
        # endregion

        # region Check new DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("New child DMA order", self.test_id))

        self.dma_2_qdl9_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl9_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit9, OrderQty=self.aggressive_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_qdl9_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child 2 DMA order on the MTF')

        er_pending_new_dma_2_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl9_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child 2 DMA order on the MTF')

        er_new_dma_2_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl9_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child 2 DMA order on the MTF')
        # endregion

        time.sleep(60)

        # region Set up PCL phase
        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr, TradingSessionSubID=4)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)
        # endregion

        time.sleep(3)

        # region check cancel 2nd dma child order on the MTF
        er_cancel_dma_2_qdl9_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl9_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_2_qdl9_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order on the MTF")
        # endregion

        # region Check that child DMA order repatriate to primary venue
        self.fix_verifier_buy.set_case_id(bca.create_event("Repatriate passive child DMA order on the Primary venue", self.test_id))

        self.dma_2_qdl8_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl8_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit8, OrderQty=self.aggressive_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_qdl8_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA order on primary venue')

        er_pending_new_dma_2_qdl8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl8_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_qdl8_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child DMA order on primary venue')

        er_new_dma_2_qdl8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl8_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_qdl8_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child DMA order on primary venue')
        # endregion

        # region Check partial fill algo order
        er_partial_fill_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_partial_fill)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partial fill')
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel dma child order on primary venue
        er_cancel_dma_2_qdl8_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl8_order, self.gateway_side_buy, self.status_cancel)
        er_cancel_dma_2_qdl8_order.change_parameters(dict(Text="order canceled"))
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_2_qdl8_order, self.key_params_specific_cancel, self.ToQuod, "Buy Side ExecReport Cancel child DMA order on primary venue")
        # endregion

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        time.sleep(5)

        # region Set up Open phase
        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)
        # endregion

        time.sleep(60)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
        rule_manager.remove_rule(self.ocr_1_rule)
