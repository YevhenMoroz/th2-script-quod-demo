import os
import time
import sched
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, Reference, OrderType, TimeInForce
from datetime import datetime, timedelta
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot

class QAP_T4685(TestCase):
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
        # endregion

        # region order parameters
        self.order_type_limit = OrderType.Limit.value
        self.tif_day = TimeInForce.Day.value
        self.tif_ioc = TimeInForce.ImmediateOrCancel.value

        self.price_ask = 40
        self.qty_ask = 100_000

        self.price_bid = 30
        self.qty_bid = 100_000

        self.last_trade_qty = 0
        self.last_trade_price = 0

        self.qty = 2_000
        self.price = 130
        self.waves = 5
        self.min_participation = 5

        self.twap_child_order_qty = '%^(36[8-9]|526)$'
        self.price_child = 29.995

        self.market_volume_1 = 10_000
        self.market_volume_2 = 5_000
        self.market_volume_3 = 6_000
        self.market_volume_4 = 9_000

        self.check_order_sequence = False
        # endregion

        # region Venue params
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_fill = Status.Fill
        self.status_cancel = Status.Cancel
        self.status_eliminated = Status.Eliminate
        self.status_replaces = Status.CancelReplace
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_8_Fill = self.data_set.get_pre_filter('pre_filer_equal_ER_fill')
        self.pre_fileter_35_G = self.data_set.get_pre_filter('pre_filer_equal_G')
        self.pre_fileter_35_8_CancelReplace = self.data_set.get_pre_filter('pre_filer_equal_ER_cancel_replace')
        self.pre_fileter_35_8_Eliminate = self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate')
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region rules
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeOnFullQty(self.fix_env1.buy_side, self.account, self.ex_destination_1)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, nos_trade_rule, ocrr_rule, ocr_rule]
        # endregion

        # region Start/EndDate for algo
        utcnow = datetime.utcnow() + timedelta(minutes=1) - timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
        end_date = (utcnow + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")
        start_date = utcnow.strftime("%Y%m%d-%H:%M:%S")
        # endregion

        # region EndDate for TradingPhases
        now = datetime.utcnow() + timedelta(minutes=1) - timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
        end_date_open = now + timedelta(minutes=5)
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open)
        trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.Open, end_date_open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(5)
        # endregion

        # region send trading phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price).set_phase(TradingPhases.Open)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        initial_order = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 300
        first_slice_20_seconds = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 280
        second_slice_20_seconds = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 230
        third_slice_20_seconds = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 170
        fouth_slice_20_seconds = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 110
        end_time_minus_5_sec = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 5
        end_time = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False)

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create TWAP Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Redburn_params()
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.twap_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, StartDate2=start_date, EndDate2=end_date, MinParticipation=self.min_participation))

        scheduler.enterabs(initial_order, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.twap_order, message_name='Sell Side Send Algo order'))

        time.sleep(2)
        # endregion

        # region Check Sell side
        scheduler.enterabs(initial_order + 3, 2, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.twap_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        pending_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        scheduler.enterabs(initial_order + 3, 3, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=pending_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        scheduler.enterabs(initial_order + 3, 4, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        # region Send Trade before 1st slice
        self.case_id_2 = bca.create_event("TWAP child order", self.test_id)

        # region Check Buy Side
        twap_dma_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        twap_dma_child_order.change_parameters(dict(Account=self.account, OrderQty=self.twap_child_order_qty, Price=self.price_child, Instrument='*', ExDestination=self.ex_destination_1))

        pending_twap_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_dma_child_order, self.gateway_side_buy, self.status_pending)

        new_twap_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_dma_child_order, self.gateway_side_buy, self.status_new)

        fill_twap_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_dma_child_order, self.gateway_side_buy, self.status_fill)
        # endregion

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trade before 1st slice", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.market_volume_1).set_phase(TradingPhases.Open)
        scheduler.enterabs(first_slice_20_seconds, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion

        # region Send Trade during 1st slice
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trade during 1st slice", self.test_id))
        self.incremental_refresh_2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.market_volume_2).set_phase(TradingPhases.Open)
        scheduler.enterabs(second_slice_20_seconds, 2, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_2))
        # endregion

        # region Send Trade during 2nd slice
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trade during 2nd slice", self.test_id))
        self.incremental_refresh_3 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.market_volume_3).set_phase(TradingPhases.Open)
        scheduler.enterabs(third_slice_20_seconds, 3, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_3))
        # endregion

        # region Send Trade during 3rd slice
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trade during 3rd slice", self.test_id))
        self.incremental_refresh_4 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.market_volume_4).set_phase(TradingPhases.Open)
        scheduler.enterabs(fouth_slice_20_seconds, 4, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_4))
        # endregion

        # region Check TWAP child orders
        # region Check 35=D of child orders
        scheduler.enterabs(end_time_minus_5_sec, 1, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[twap_dma_child_order, twap_dma_child_order, twap_dma_child_order, twap_dma_child_order, twap_dma_child_order], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.FromQuod, pre_filter=self.pre_fileter_35_D, check_order=self.check_order_sequence))
        # endregion

        # region Check Pending New and New execution report for child orders
        scheduler.enterabs(end_time_minus_5_sec, 2, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[pending_twap_dma_child_order_params, pending_twap_dma_child_order_params, pending_twap_dma_child_order_params, pending_twap_dma_child_order_params, pending_twap_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Pending_new, check_order=self.check_order_sequence))

        scheduler.enterabs(end_time_minus_5_sec, 3, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[new_twap_dma_child_order_params, new_twap_dma_child_order_params, new_twap_dma_child_order_params, new_twap_dma_child_order_params, new_twap_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_New, check_order=self.check_order_sequence))
        # endregion

        self.fix_verifier_buy.set_case_id(bca.create_event("Check Auction algo child order Buy Side NewOrderSingle, Pending New, New and Fill", self.case_id_2))
        scheduler.enterabs(end_time_minus_5_sec, 4, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[fill_twap_dma_child_order_params, fill_twap_dma_child_order_params, fill_twap_dma_child_order_params, fill_twap_dma_child_order_params, fill_twap_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Fill, check_order=self.check_order_sequence))
        # endregion

        # region Change phase from OPN to PCL
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Change phase from OPN to PCL", self.test_id))
        self.incremental_refresh_5 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price).set_phase(TradingPhases.PreClosed)
        scheduler.enterabs(end_time, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_5))
        # endregion

        scheduler.run()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order
        self.case_id_3 = bca.create_event("Fill Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_3)

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        cancel_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(cancel_twap_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Fill')
        # endregion

