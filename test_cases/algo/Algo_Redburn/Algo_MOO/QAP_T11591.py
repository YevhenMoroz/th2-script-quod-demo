import os
import sched
import time

from pathlib import Path
from datetime import datetime, timedelta, timezone

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, RBCustomTags
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T11591(TestCase):
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
        # endregion

        # region order parameters
        self.indicative_volume = 2000
        self.indicative_volume_1 = 3000
        self.indicative_price = 30
        self.percentage_volume = 10
        
        self.qty = 1_000_000
        self.price = 30
        self.would_price = 29

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.qty_0 = self.price_0 = 0

        self.auction_child_qty_1_check = AFM.get_child_qty_for_auction(self.indicative_volume, self.percentage_volume, self.qty) #223
        self.auction_child_qty_2_check = AFM.get_bi_lateral_auction_qty(self.indicative_volume, self.percentage_volume, self.auction_child_qty_1_check, self.qty) #198
        self.auction_child_qty_3_check = AFM.get_bi_lateral_auction_qty(self.indicative_volume, self.percentage_volume, self.auction_child_qty_2_check, self.qty) #201
        self.auction_child_qty_4_check = AFM.get_bi_lateral_auction_qty(self.indicative_volume, self.percentage_volume, self.auction_child_qty_3_check, self.qty) #200
        self.auction_child_qty_5_check = AFM.get_bi_lateral_auction_qty(self.indicative_volume, self.percentage_volume, self.auction_child_qty_4_check, self.qty) #200

        self.auc_child_qty_1 = self.auction_child_qty_1_check   #223
        self.auc_child_qty_2 = self.auction_child_qty_3_check - self.auction_child_qty_2_check  #3
        self.auc_child_qty_3 = self.auction_child_qty_4_check - self.auction_child_qty_2_check  #2
        self.auction_would_child_qty = self.qty - self.auction_child_qty_2_check - self.auc_child_qty_3   #999800

        self.tif_ato = TimeInForce.AtTheOpening.value
        self.check_order_sequence = False
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reached_uncross = Status.ReachedUncross
        self.status_eliminate = Status.Eliminate
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        # self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # self.client = self.data_set.get_client_by_name("client_2")
        # self.account = self.data_set.get_account_by_name("account_2")
        # self.mic = self.data_set.get_mic_by_name("mic_1")
        # self.listing_id = self.data_set.get_listing_id_by_name("listing_36")

        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_21")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_18")
        self.mic = self.data_set.get_mic_by_name("mic_31")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_37")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile2")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_8_Eliminate = self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate')
        self.pre_fileter_35_8_Cancel_Replace = self.data_set.get_pre_filter('pre_filer_equal_ER_cancel_replace')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)        
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportAll(self.fix_env1.buy_side, self.account, self.mic)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        self.rule_list = [nos_rule, ocr_rule, ocrr_rule]
        # endregion

        # region EndDate for TradingPhases
        self.start_date = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.start_date = self.start_date - timedelta(seconds=self.start_date.second, microseconds=self.start_date.microsecond) + timedelta(minutes=1)
        self.end_date_pre_open = (self.start_date + timedelta(minutes=2))
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.PreOpen)
        trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.PreOpen, self.end_date_pre_open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Clear IAV
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send IAV and trading phase - PreOpen", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.qty_0).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.price_0).set_phase(TradingPhases.PreOpen)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion
        
        # region Send MarketData for POV order
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send IAV and trading phase - PreOpen", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price).set_phase(TradingPhases.PreOpen)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        initial_slice = self.end_date_pre_open.timestamp() - 120
        end_phase_minus_5 = self.end_date_pre_open.timestamp() - 4
        end_phase_time_plus_4 = self.end_date_pre_open.timestamp() + 4
        random_uncross = self.end_date_pre_open.timestamp() + 8

        # region Send NewOrderSingle (35=D) for
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        scheduler.enterabs(initial_slice, 1, self.fix_manager_sell.set_case_id, kwargs=dict(case_id=case_id_1))

        self.auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOO_Would_params()
        self.auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.auction_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, TriggerPriceRed=self.would_price))
        scheduler.enterabs(initial_slice, 2, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.auction_algo))

        # region Check Sell side
        self.case_id_2 = bca.create_event("Auction child order", self.test_id)
        scheduler.enterabs(initial_slice, 3, self.fix_verifier_sell.set_case_id, kwargs=dict(case_id=self.case_id_2))

        scheduler.enterabs(initial_slice, 4, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.auction_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_pending)
        pending_auction_order_params.change_parameters(dict(TimeInForce=self.tif_ato))
        scheduler.enterabs(initial_slice, 5, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_new)
        new_auction_order_params.change_parameters(dict(TimeInForce=self.tif_ato))
        scheduler.enterabs(initial_slice, 6, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        # region Check Auction DMA child order 1
        self.case_id_3 = bca.create_event("Auction DMA child order 1", self.test_id)
        scheduler.enterabs(end_phase_time_plus_4, 1, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=self.case_id_3))

        self.auction_dma_child_order_1 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.auction_dma_child_order_1.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.auc_child_qty_1, Price=self.price, TimeInForce=self.tif_ato, Instrument=self.instrument))
        scheduler.enterabs(end_phase_time_plus_4, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.auction_dma_child_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Auction child order 1'))

        pending_auction_dma_child_order_1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order_1, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(end_phase_time_plus_4, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_auction_dma_child_order_1, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Auction child order 1'))

        new_auction_dma_child_order_1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order_1, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(end_phase_time_plus_4, 4, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_auction_dma_child_order_1, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Auction child order 1'))
        # endregion
        
        # region Check Auction DMA child order 2
        self.case_id_4 = bca.create_event("Auction DMA child order 2", self.test_id)
        scheduler.enterabs(end_phase_time_plus_4, 5, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=self.case_id_4))

        self.auction_dma_child_order_2 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.auction_dma_child_order_2.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.auc_child_qty_1, Price=self.price, TimeInForce=self.tif_ato, Instrument=self.instrument))
        scheduler.enterabs(end_phase_time_plus_4, 6, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.auction_dma_child_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Auction child order 2'))

        pending_auction_dma_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order_2, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(end_phase_time_plus_4, 7, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_auction_dma_child_order_2, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Auction child order 2'))

        new_auction_dma_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order_2, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(end_phase_time_plus_4, 8, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_auction_dma_child_order_2, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Auction child order 2'))
        # endregion
        
        # region Check Auction Would child order
        self.case_id_5 = bca.create_event("Auction Would child order", self.test_id)
        scheduler.enterabs(end_phase_time_plus_4, 9, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=self.case_id_5))

        self.auction_would_child_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.auction_would_child_order.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.auction_would_child_qty, Price=self.would_price, TimeInForce=self.tif_ato, Instrument=self.instrument))
        scheduler.enterabs(end_phase_time_plus_4, 10, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.auction_would_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Auction Would child order'))

        pending_auction_would_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_would_child_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(end_phase_time_plus_4, 11, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_auction_would_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Auction Would child order'))

        new_auction_would_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_would_child_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(end_phase_time_plus_4, 12, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_auction_would_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Auction Would child order'))
        # endregion

        # region Send new Indicative price to trigger an Auction child orders modification phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send new Indicative price", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume_1).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price).set_phase(TradingPhases.PreOpen)
        scheduler.enterabs(end_phase_minus_5, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion

        # region Send OPN phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send OPN phase during random uncross", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', 0).set_phase(TradingPhases.Open)
        scheduler.enterabs(random_uncross, 2, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion
        
        scheduler.run()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)
        # region Cancel Algo Order
        case_id_6 = bca.create_event("Reached uncross Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_6)
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

        reached_uncross_auction_algo_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_reached_uncross)
        reached_uncross_auction_algo_order.change_parameters(dict(TimeInForce=self.tif_ato, LastMkt=self.mic))
        self.fix_verifier_sell.check_fix_message(reached_uncross_auction_algo_order, key_parameters=self.key_params, message_name='Sell side ExecReport Reached uncross')