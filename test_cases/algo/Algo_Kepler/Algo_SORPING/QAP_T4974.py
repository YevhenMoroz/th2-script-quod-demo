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
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4974(TestCase):
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
        self.qty = 100
        self.price = 25
        self.dark_price = 44
        self.traded_qty = 0
        self.qty_for_md = 1000
        self.price_ask_qdl8 = 44
        self.price_bid = 30
        self.price_ask_qdl9 = 40
        self.price_ask_qdl10 = 40
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_6.value
        self.sell = constants.OrderSide.Sell.value
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
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_16")
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
        self.listing_id_qdl8 = self.data_set.get_listing_id_by_name("listing_20")
        self.listing_id_qdl9 = self.data_set.get_listing_id_by_name("listing_21")
        self.listing_id_qdl10 = self.data_set.get_listing_id_by_name("listing_22")
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
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp1, False, self.traded_qty, self.dark_price)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp2, False, self.traded_qty, self.dark_price)
        nos_3_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, True, self.qty, self.price_bid)
        self.rule_list = [nos_1_ioc_rule, nos_2_ioc_rule, nos_3_ioc_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl8 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl8, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)

        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl9 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl9, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl9, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl9)

        market_data_snap_shot_qdl9 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl9, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl9.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl9)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl10 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl10, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl10.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl10.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl10, MDEntrySize=self.qty_for_md)
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
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Side=self.sell, Instrument=self.instrument))

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

        # region Check dark childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        # region Check child DMA order on venue QUODPKP1
        self.dma_qdpkp1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_SORPING_params()
        self.dma_qdpkp1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp1, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_ioc, Side=self.sell))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdpkp1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        time.sleep(2)

        er_eliminate_dma_qdpkp1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp1_order, self.gateway_side_buy, self.status_eliminate)
        er_eliminate_dma_qdpkp1_order.add_tag(dict(ExDestination=self.ex_destination_quoddkp1))
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_dma_qdpkp1_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 1 order")
        # endregion

        # region Check child DMA order on venue QUODPKP2
        self.dma_qdpkp2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_SORPING_params()
        self.dma_qdpkp2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quoddkp2, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_ioc, Side=self.sell))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdpkp2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_eliminate_dma_qdpkp2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdpkp2_order, self.gateway_side_buy, self.status_eliminate)
        er_eliminate_dma_qdpkp2_order.add_tag(dict(ExDestination=self.ex_destination_quoddkp2))
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_dma_qdpkp2_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 2 order")
        # endregion
        # endregion

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order", self.test_id))

        self.dma_qdl9_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qdl9_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit9, OrderQty=self.qty, Price=self.price_bid, TimeInForce=self.tif_ioc, Side=self.sell, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdl9_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order')

        er_pending_new_dma_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_qdl9_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit9))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        er_new_dma_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_new)
        er_new_dma_qdl9_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit9))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion

        # region check fill fourth dma child order
        er_fill_dma_qdl9_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_qdl9_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Fill child DMA 3 order")
        # endregion

        er_fill_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(er_fill_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
