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


class QAP_T8855(TestCase):
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
        self.min_qty = 700
        self.display_qty = 750
        self.price = 45
        self.dark_price = 30
        self.traded_qty_dark = 0
        self.traded_qty_lit = 1000
        self.passive_child_qty = self.qty - self.traded_qty_lit
        self.qty_for_md = 1000
        self.price_ask_qdl6 = 40
        self.price_bid = 30
        self.price_ask_qdl7 = 50
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.delay = 0
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_6.value
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_13")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit6 = self.data_set.get_mic_by_name("mic_18")
        self.ex_destination_quoddkp1 = self.data_set.get_mic_by_name("mic_14")
        self.ex_destination_quoddkp2 = self.data_set.get_mic_by_name("mic_15")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl6 = self.data_set.get_listing_id_by_name("listing_11")
        self.listing_id_qdl7 = self.data_set.get_listing_id_by_name("listing_12")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp1, False, self.traded_qty_dark, self.dark_price)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp2, False, self.traded_qty_dark, self.dark_price)
        nos_3_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit6, True, self.traded_qty_lit, self.price_ask_qdl6, 1000)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit6, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit6, True)
        self.rule_list = [nos_1_ioc_rule, nos_2_ioc_rule, nos_3_ioc_rule, nos_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl6 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl6, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl6, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl6)

        market_data_snap_shot_qdl6 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl6, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl6)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl7 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl7, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl7.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl7.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl7, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl7)

        market_data_snap_shot_qdl7 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl7, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl7.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl7)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument)).add_tag(dict(MinQty=self.min_qty, DisplayInstruction=dict(DisplayQty=self.display_qty)))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(2)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_qdl6 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl6, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl7, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl6)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check dark childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        # region Check child DMA order on venue QUODPKP1
        self.dma_qdpkp1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_SORPING_params()
        self.dma_qdpkp1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp1, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_ioc)).add_tag(dict(MinQty=self.min_qty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdpkp1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Dark Child DMA 1 order')

        time.sleep(2)

        er_eliminate_dma_qdpkp1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp1_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_dma_qdpkp1_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate Dark child DMA 1 order")
        # endregion

        # region Check child DMA order on venue QUODPKP2
        self.dma_qdpkp2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_SORPING_params()
        self.dma_qdpkp2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp2, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_ioc)).add_tag(dict(MinQty=self.min_qty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdpkp2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Dark Child DMA 2 order')

        er_eliminate_dma_qdpkp2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp2_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_dma_qdpkp2_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate Dark child DMA 2 order")
        # endregion
        # endregion

        # region Check Aggressive Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA orders", self.test_id))

        self.dma_1_qdl6_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl6_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit6, OrderQty=self.traded_qty_lit, Price=self.price_ask_qdl6, Instrument=self.instrument, TimeInForce=self.tif_ioc)).add_tag(dict(MinQty=self.min_qty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_qdl6_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_qdl6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl6_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_qdl6_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Lit Child DMA 1 order')

        er_new_dma_1_qdl6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl6_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_qdl6_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child Lit DMA 1 order')

        er_fill_dma_1_qdl6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl6_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_1_qdl6_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Lit Child DMA 1 order')
        # endregion

        # region Check Passive Lit child DMA order
        self.dma_2_qdl6_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl6_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit6, OrderQty=self.passive_child_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_qdl6_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_2_qdl6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl6_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_qdl6_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Lit Child DMA 1 order')

        er_new_dma_2_qdl6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl6_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_qdl6_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child Lit DMA 1 order')
        # endregion

        # region Check partial fill parent order
        er_partial_fill_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_partial_fill)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partial fill')
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel third dma child order
        er_cancel_dma_2_qdl6_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl6_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_2_qdl6_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel Lit passive Child DMA order on venue qdl6: OldQty=11000, price=52")
        # endregion

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
