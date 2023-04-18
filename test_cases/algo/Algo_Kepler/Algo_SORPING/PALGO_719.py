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
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T10981(TestCase):
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
        self.qty = 100000
        self.price = 39
        self.dark_price = 44
        self.traded_qty = 0
        self.qty_for_md = 1000
        self.price_ask_qdl8 = 44
        self.price_bid = 30
        self.price_ask_qdl9 = 40
        self.price_ask_qdl10 = 40
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.text = "X: Expired"
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_9.value
        self.sell = constants.OrderSide.Sell.value

        now = datetime.today() - timedelta(hours=3)
        self.ExpireDate=(now + timedelta(days=2)).strftime("%Y%m%d")
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
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_dfd_mapping_buy_side.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        # endregion

        # region Compare message params
        self.exec_type = "Eliminated"
        self.elimination_handling = "StopChildCreation"
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_eliminate_rule = rule_manager.add_NewOrderSingle_ExecutionReport_Eliminate(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, self.price, text=self.text, delay=2000)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit8, self.price)
        nos_dfd_rule = rule_manager.add_NewOrderSingle_ExecutionReport_DoneForDay(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit8, self.price, delay=10000)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit9, True)
        self.rule_list = [nos_eliminate_rule, nos_1_rule, ocr_1_rule, nos_2_rule, nos_dfd_rule]
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
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Side=self.sell, Instrument=self.instrument, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate=self.ExpireDate))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl8 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=39.5, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl8, MDEntrySize=self.qty_for_md)
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

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order on the MTF", self.test_id))

        self.dma_qdl9_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qdl9_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit9, OrderQty=self.qty, Price=self.price, Side=self.sell, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdl9_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA order on MTF')

        er_pending_new_dma_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order on MTF')

        er_new_dma_qdl9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qdl9_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order on MTF')
        # endregion

        # region Set up PCL phase
        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr, TradingSessionSubID=4)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)
        # endregion

        time.sleep(3)

        # region check cancel dma child order on the MTF
        er_cancel_dma_qdl9_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl9_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_qdl9_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA order on the MTF")
        # endregion

        # region Check that child DMA order repatriates to primary venue
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order on the Primary venue", self.test_id))

        self.dma_qdl8_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qdl8_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit8, OrderQty=self.qty, Price=self.price, Side=self.sell, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdl8_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA order on primary venue')

        er_pending_new_dma_qdl8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl8_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qdl8_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order on primary venue')

        er_new_dma_qdl8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl8_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qdl8_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order on primary venue')
        # endregion

        time.sleep(5)

        # region Set up CLO phase
        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr, TradingSessionSubID=1, SecurityTradingStatus=2)
        # self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)
        # endregion

        time.sleep(2)

        # region check eliminate with DFD second dma child order
        er_eliminate_with_dfd_dma_qdl8_order = FixMessageExecutionReportAlgo().set_params_for_nos_dfd_rule(self.dma_qdl8_order)
        self.fix_verifier_buy.check_fix_message_kepler(er_eliminate_with_dfd_dma_qdl8_order, self.key_params_ER_eliminate_child, self.ToQuod, "Buy Side ExecReport Eliminate with DFD child DMA 2 order")
        # endregion

        # region Check that the parent order is eliminated
        er_eliminate_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_eliminate)
        er_eliminate_SORPING_order_params.add_tag(dict(LastMkt='*', Text='Passive order elimination received on QUODLIT8 (100 @ EUR 39.0000) - DoneForDay'))
        self.fix_verifier_sell.check_fix_message(er_eliminate_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion

        # region Check Read log
        #time.sleep(70)

        # compare_message = ReadLogMessageAlgo().set_compare_message_for_check_dfd_mapping_buy_side()
        # compare_message.change_parameters(dict(ClOrdID='*', ExecType=self.exec_type, EliminationHandling=self.elimination_handling))
        #
        # self.read_log_verifier.set_case_id(bca.create_event("ReadLog", self.test_id))
        # self.read_log_verifier.check_read_log_message(compare_message)
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Set up the Open phase
        market_data_snap_shot_qdl8 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl8, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl8.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        # self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl8)
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
