import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T5003(TestCase):
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
        self.qty = 15_000
        self.price = 25
        self.dark_price = 44
        self.traded_qty = 0
        self.cum_qty = 3000
        self.qty_passive_child = 13_000
        self.dec_qty_passive_child = 12_000
        self.qty_for_md = 1000
        self.price_ask_qdl1 = 44
        self.price_bid_qdl1 = 30
        self.price_ask_qdl2 = 40
        self.price_bid_qdl2 = 28
        self.new_price_bid = 20
        self.new_price_bid_qdl2 = 27
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.tif_iok = constants.TimeInForce.ImmediateOrCancel.value
        self.side = constants.OrderSide.Sell.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        self.status_partial_fill = Status.PartialFill
        self.status_eliminate = Status.Eliminate
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
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
        self.ex_destination_quoddkp1 = self.data_set.get_mic_by_name("mic_14")
        self.ex_destination_quoddkp2 = self.data_set.get_mic_by_name("mic_15")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_ER_partially_fill_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_Partially_Fill_Parent")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_fill_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_Reject_Eliminate_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_dark_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp1, False, self.traded_qty, self.dark_price)
        nos_dark_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp2, False, self.traded_qty, self.dark_price)
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True, self.qty_for_md, self.price_bid_qdl1)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit2, True, self.qty_for_md, self.price_bid_qdl2)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_3_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit2, True, self.qty_for_md, self.new_price_bid_qdl2)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True)
        self.rule_list = [nos_dark_1_ioc_rule, nos_dark_2_ioc_rule, nos_1_ioc_rule, nos_2_ioc_rule, nos_rule, nos_3_ioc_rule, ocrr_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl1, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl1, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl2, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl2, MDEntrySize=self.qty_for_md)
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
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Side=self.side))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # Delays on sim affect this. Set up time.sleep from 0 to 2

        time.sleep(1)

        # region Update_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.new_price_bid_qdl2, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl1, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.new_price_bid_qdl2, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl2, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(2)

        # region second update
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update 2 Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.new_price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl1, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update 2 Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.new_price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl2, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Check dark childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        # region Check child DMA order on venue QUODPKP1
        self.dma_qdpkp1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_qdpkp1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp1, Side=self.side, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_qdpkp1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_eliminate_dma_qdpkp1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp1_order, self.gateway_side_buy, self.status_eliminate)
        er_eliminate_dma_qdpkp1_order.add_tag(dict(ExDestination=self.ex_destination_quoddkp1))
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_qdpkp1_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 1 order")
        # endregion

        # region Check child DMA order on venue QUODPKP2
        self.dma_qdpkp2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_qdpkp2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp2, Side=self.side, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_qdpkp2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_eliminate_dma_qdpkp2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp2_order, self.gateway_side_buy, self.status_eliminate)
        er_eliminate_dma_qdpkp2_order.add_tag(dict(ExDestination=self.ex_destination_quoddkp2))
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_qdpkp2_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 2 order")
        # endregion

        # region Check 1 child DMA order on venue QUODLIT1
        self.fix_verifier_buy.set_case_id(bca.create_event("Aggressive child DMA orders", self.test_id))

        self.dma_1_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, Side=self.side, OrderQty=self.qty_for_md, Price=self.price_bid_qdl1, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_1_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order')

        er_fill_dma_qdl1__order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_qdl1__order, self.key_params_ER_fill_child, self.ToQuod, "Buy Side ExecReport Fill child DMA 3 order")
        # endregion

        # region Check 1 child DMA order on venue QUODLIT2
        self.dma_1_qdl2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit2, Side=self.side, OrderQty=self.qty_for_md, Price=self.price_bid_qdl2, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_1_qdl2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 4 order')

        er_fill_dma_1_qdl2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl2_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_1_qdl2_order, self.key_params_ER_fill_child, self.ToQuod, "Buy Side ExecReport Fill child DMA 4 order")
        # endregion

        # region Check 2 child DMA order on venue QUODLIT1
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive child DMA order", self.test_id))
        self.dma_2_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, Side=self.side, OrderQty=self.qty_passive_child, Price=self.price))
        self.fix_verifier_buy.check_fix_message(self.dma_2_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 5 order')

        er_pending_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 5 order')

        er_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_new)
        er_new_dma_2_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 5 order')
        # endregion

        # region Check 2 child DMA order on venue QUODLIT2
        self.fix_verifier_buy.set_case_id(bca.create_event("Grep liquidity: child DMA order", self.test_id))
        self.dma_2_qdl2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit2, Side=self.side, OrderQty=self.qty_for_md, Price=self.new_price_bid_qdl2, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_2_qdl2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 6 order')

        er_fill_dma_2_qdl2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl2_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_2_qdl2_order, self.key_params_ER_fill_child, self.ToQuod, "Buy Side ExecReport fill child DMA 6 order")
        # endregion

        # region Check replace 2 child DMA order on venue QUODLIT1
        er_replace_dma_2_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_cancel_replace)
        er_replace_dma_2_qdl1_order.change_parameters(dict(OrderQty=self.dec_qty_passive_child))
        self.fix_verifier_buy.check_fix_message(er_replace_dma_2_qdl1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Replace child DMA 5 order")
        # endregion

        # region Check Partially fill parent order
        er_partiall_fill_SORPING_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_partial_fill)
        er_partiall_fill_SORPING_order.change_parameters(dict(LastPx=self.new_price_bid_qdl2, CumQty=self.cum_qty, LeavesQty=self.dec_qty_passive_child, LastQty=self.qty_for_md))
        self.fix_verifier_sell.check_fix_message(er_partiall_fill_SORPING_order, key_parameters=self.key_params_ER_partially_fill_parent, message_name='Sell side ExecReport Partially fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel third dma child order
        er_cancel_dma_2_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_cancel)
        er_cancel_dma_2_qdl1_order.change_parameters(dict(OrderQty=self.dec_qty_passive_child))
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_2_qdl1_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 5 order")
        # endregion

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_cancel)
        er_cancel_SORPING_order_params.change_parameters(dict(CumQty=self.cum_qty, CxlQty=self.dec_qty_passive_child, AvgPx='*'))
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
