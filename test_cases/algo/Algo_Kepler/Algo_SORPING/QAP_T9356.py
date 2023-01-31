import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo


class QAP_T9356(TestCase):
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
        self.price = 3.2
        self.traded_qty = 0
        self.qty_for_md = 100
        self.price_ask = 3
        self.price_bid = 2.9
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.trading_phase = 4
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_8.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_9")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_xpar = self.data_set.get_listing_id_by_name("listing_6")
        self.listing_id_bats = self.data_set.get_listing_id_by_name("listing_32")
        self.listing_id_chix = self.data_set.get_listing_id_by_name("listing_33")
        self.listing_id_janestreet = self.data_set.get_listing_id_by_name("listing_34")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_15")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_fill_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_order_event.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        self.key_params_readlog = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_order_event")
        # endregion

        # region Compare message parameters
        self.text_1 = "PCL phase, sending lit"
        self.text_2 = "Phase of the reference market is PCL"
        self.text_3 = "passive goes to the default market"
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, True)
        self.rule_list = [nos_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr, TradingSessionSubID=self.trading_phase)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xpar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_chix, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        market_data_snap_shot_xpar = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_chix, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        market_data_snap_shot_bats = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_bats, self.fix_env1.feed_handler)
        market_data_snap_shot_bats.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_bats.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_bats)

        market_data_snap_shot_bats = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_bats, self.fix_env1.feed_handler)
        market_data_snap_shot_bats.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_bats)

        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        market_data_snap_shot_trqx = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        market_data_snap_shot_janestreet = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_janestreet, self.fix_env1.feed_handler)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_janestreet)

        market_data_snap_shot_janestreet = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_janestreet, self.fix_env1.feed_handler)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_janestreet)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ClientAlgoPolicyID=self.algopolicy))

        responce = self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)
        parent_SORPING_order_id = responce[0].get_parameter('ExecID')
        parent_SORPING_order_id_list = list(parent_SORPING_order_id)
        parent_SORPING_order_id_list[-1] = 2
        multilisted_algo_child_order_id = "".join(map(str, parent_SORPING_order_id_list))

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message_1 = ReadLogMessageAlgo().set_compare_message_for_check_order_event()
        compare_message_1.change_parameters(dict(OrderId=parent_SORPING_order_id, Text=self.text_1))

        compare_message_2 = ReadLogMessageAlgo().set_compare_message_for_check_order_event()
        compare_message_2.change_parameters(dict(OrderId=multilisted_algo_child_order_id, Text=self.text_2))

        compare_message_3 = ReadLogMessageAlgo().set_compare_message_for_check_order_event()
        compare_message_3.change_parameters(dict(OrderId=multilisted_algo_child_order_id, Text=self.text_3))

        self.read_log_verifier.set_case_id(bca.create_event("Check skipping DarkPhase", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message_1, self.key_params_readlog)

        self.read_log_verifier.set_case_id(bca.create_event("Check that primary venue goes to the PCL phase", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message_2, self.key_params_readlog)

        self.read_log_verifier.set_case_id(bca.create_event("Check that passive goes to the default market", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message_3, self.key_params_readlog)
        # endregion

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order", self.test_id))

        self.dma_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Lit Child DMA order')

        er_pending_new_dma_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Lit Child DMA order')

        er_new_dma_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Lit Child DMA order')
        # endregion

        # region Check these are no dark childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Check these are no dark childs", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.dma_xpar_order], [None], self.FromQuod)
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel Lit Child DMA order")

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        time.sleep(5)

        # region return TradingStatus=T for Paris
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

