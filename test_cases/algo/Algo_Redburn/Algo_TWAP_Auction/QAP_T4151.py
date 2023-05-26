import os
import sched
import time

from pathlib import Path


from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from datetime import datetime, timedelta, timezone
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T4151(TestCase):
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
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        # endregion

        # region order parameters
        self.qty = 1_000_000
        self.indicative_volume = 0
        self.price = 130

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.last_trade_qty = 0
        self.last_trade_price = 0

        self.navigator_limit_price = 25
        self.navigator_percentage = 70

        self.navigator_child_qty = AFM.get_twap_nav_child_qty(self.qty, 5, nav_percentage=self.navigator_percentage)
        self.all_twap_slices_qty = AFM.get_all_twap_slices(self.qty, 5)
        self.passive_phase_price = self.price_bid - 0.005

        self.check_order_sequence = False

        self.pre_filter_cancel = self.data_set.get_pre_filter('pre_filer_equal_ER_canceled')
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        # self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # self.client = self.data_set.get_client_by_name("client_2")
        # self.account = self.data_set.get_account_by_name("account_2")
        # self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        # self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        #
        # self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        # endregion

        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_38")
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_21")
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_47")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_58")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile3")

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, False, 0, self.price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.passive_phase_price)
        nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.navigator_limit_price)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_xpar)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_xpar, True)
        self.rule_list = [nos_rule, nos_rule2, nos_rule3, ocr_rule, ocrr_rule, cancel_rule]
        # endregion

        self.send_algo = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.send_algo = self.send_algo - timedelta(seconds=self.send_algo.second, microseconds=self.send_algo.microsecond) + timedelta(minutes=1)
        self.end_phase = (self.send_algo + timedelta(minutes=6))
        start_date = self.send_algo.strftime("%Y%m%d-%H:%M:%S")

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open, TimeSlot.current_phase, duration=7)
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid, MDEntryPositionNo=1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.last_trade_price, MDEntrySize=self.last_trade_qty)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion
        
        scheduler = sched.scheduler(time.time, time.sleep)
        send_algo_order_checkpoint = self.end_phase.timestamp() - 360
        send_incremental_refresh_intr_auc_checkpoint = self.end_phase.timestamp() - 355
        twap_and_nav_child_orders_checkpoint = self.end_phase.timestamp() - 350
        send_incremental_refresh_opn_checkpoint = self.end_phase.timestamp() - 340
        send_twap_child_2_checkpoint = self.end_phase.timestamp() - 280

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create TWAP Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Send TWAP algo
        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Navigator_params()
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_xpar))
        self.twap_order.update_fields_in_component('QuodFlatParameters', dict(NavigatorPercentage=self.navigator_percentage, NavigatorLimitPrice=self.navigator_limit_price, StartDate2=start_date, Waves=5))
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.twap_order))
        # endregion

        # region Check Sell side
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.twap_order, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        er_pending_new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        scheduler.enterabs(send_algo_order_checkpoint, 2, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=er_pending_new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        er_new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        scheduler.enterabs(send_algo_order_checkpoint, 3, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=er_new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        time.sleep(5)

        self.incremental_refresh_pre_auction = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative() \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler) \
            .set_phase(TradingPhases.Auction)

        time.sleep(3)
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Auction", self.test_id))
        scheduler.enterabs(send_incremental_refresh_intr_auc_checkpoint, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_pre_auction))

        # region Check TWAP slice 1 order
        time.sleep(3)
        case_id_2 = bca.create_event("Check TWAP slice 1 order", self.test_id)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 1, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=case_id_2))

        twap_slice_1_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        twap_slice_1_order.change_parameters(dict(Account=self.account, OrderQty=self.all_twap_slices_qty[0], Price=self.passive_phase_price, Instrument='*', ExDestination=self.ex_destination_xpar))
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=twap_slice_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 1'))

        pending_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_slice_1_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_twap_slice_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 1'))

        new_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_slice_1_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 4, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_twap_slice_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 1'))

        cancel_twap_slice_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_slice_1_order, self.gateway_side_buy, self.status_cancel)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 5, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[cancel_twap_slice_1_order], key_parameters_list=[self.key_params], direction=self.ToQuod, pre_filter=self.pre_filter_cancel, message_name='Buy side ExecReport Canceled TWAP child order', check_order=self.check_order_sequence))
        # endregion

        # region Check Navigator child order
        self.case_id_3 = bca.create_event("Check that TWAP Navigator child 1", self.test_id)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 6, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=self.case_id_3))

        self.navigator_child = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.navigator_child.change_parameters(dict(Account=self.account, OrderQty=self.navigator_child_qty, Price=self.navigator_limit_price, Instrument='*', ExDestination=self.ex_destination_xpar))
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 7, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.navigator_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Navigator Child 1'))

        pending_navigator_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 8, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_navigator_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Navigator Child 1'))

        new_navigator_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(twap_and_nav_child_orders_checkpoint, 9, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_navigator_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Navigator Child 1'))
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to change AUC phase into OPN", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid, MDEntryPositionNo=1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.last_trade_price, MDEntrySize=self.last_trade_qty)
        scheduler.enterabs(send_incremental_refresh_opn_checkpoint, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=market_data_incremental_par))
        # endregion

        self.case_id_4 = bca.create_event("Check TWAP slice 2 order", self.test_id)
        scheduler.enterabs(send_twap_child_2_checkpoint, 1, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=self.case_id_4))

        self.twap_slice_2_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.twap_slice_2_order.change_parameters(dict(Account=self.account, OrderQty=self.all_twap_slices_qty[1], Price=self.passive_phase_price, Instrument='*', ExDestination=self.ex_destination_xpar))
        scheduler.enterabs(send_twap_child_2_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.twap_slice_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 2'))

        pending_twap_slice_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_2_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(send_twap_child_2_checkpoint, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_twap_slice_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 2'))

        new_twap_slice_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_2_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(send_twap_child_2_checkpoint, 4, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_twap_slice_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 2'))

        scheduler.run()

        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)

        # region Cancel Algo Order
        case_id_5 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_5)
        cancel_request_auction_order = FixMessageOrderCancelRequest(self.twap_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_5)
        # endregion

        time.sleep(2)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        self.fix_verifier_buy.set_case_id(self.case_id_3)
        cancel_navigator_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_navigator_child_order, self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Canceled Navigator child order')

        self.fix_verifier_buy.set_case_id(self.case_id_4)
        cancel_twap_slice_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_2_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_twap_slice_2_order, self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Canceled TWAP child 2 order')

        er_cancel_twap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_twap_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')