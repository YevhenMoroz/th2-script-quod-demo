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
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T4533(TestCase):
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
        self.indicative_volume = 1000000
        self.percentage_volume = 10
        self.save_for_close_shares = 900000

        self.qty = 1_000_000
        self.price = 35

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.auction_child_qty = AFM.get_child_qty_for_auction(self.indicative_volume, self.percentage_volume, self.qty)
        self.check_pov_qty_child = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)
        self.pov_qty_child = AFM.get_avaible_qty_with_save_for_close_shares(self.qty, self.save_for_close_shares, self.check_pov_qty_child)

        self.tif_atc = TimeInForce.AtTheClose.value
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_bid)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_rule2, ocr_rule, ocrr_rule,  cancel_rule]
        # endregion

        # region EndDate for TradingPhases
        self.start_date = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.start_date = self.start_date - timedelta(seconds=self.start_date.second, microseconds=self.start_date.microsecond) + timedelta(minutes=1)
        self.end_date_open = (self.start_date + timedelta(minutes=1))
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open)
        trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.Open, self.end_date_open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', 0).update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion
        
        # region Send MarketData for POV order
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid, MDEntryPositionNo=1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        initial_slice = self.end_date_open.timestamp() - 60
        end_time_minus_1_min = self.end_date_open.timestamp() + 3
        end_time = self.end_date_open.timestamp() + 10

        # region Send NewOrderSingle (35=D) for
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_MOC_Auction_params()
        self.pov_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.pov_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, SaveForCloseShares=self.save_for_close_shares))
        scheduler.enterabs(initial_slice, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.pov_algo))

        # region Check Sell side
        self.case_id_2 = bca.create_event("POV child order", self.test_id)

        scheduler.enterabs(initial_slice, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.pov_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_pending)
        scheduler.enterabs(initial_slice, 2, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_new)
        scheduler.enterabs(initial_slice, 3, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        # region Check POV child order
        passive_child_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_1.change_parameters(dict(Account=self.account, OrderQty=self.pov_qty_child, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_1))
        scheduler.enterabs(end_time_minus_1_min, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=passive_child_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 1'))

        pending_passive_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(end_time_minus_1_min, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_passive_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 1'))

        new_passive_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(end_time_minus_1_min, 4, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_passive_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 1'))
        
        self.fix_verifier_buy.set_case_id(bca.create_event("Check POV child order Buy Side NewOrderSingle, Pending New, New and Cancel", self.case_id_2))
        cancel_auction_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_cancel)
        scheduler.enterabs(end_time_minus_1_min, 5, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=cancel_auction_dma_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Canceled Auction child order'))
        # endregion

        # region Send PCL phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send OPN phase during random uncross", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).set_phase(TradingPhases.PreClosed)
        scheduler.enterabs(end_time, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion
        
        scheduler.run()

        # region Check Auction DMA child order
        self.case_id_3 = bca.create_event("Auction DMA child order", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_3)

        self.auction_dma_child_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.auction_dma_child_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.auction_child_qty, Price=self.price, TimeInForce=self.tif_atc, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(fix_message=self.auction_dma_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Auction child order')

        pending_auction_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(fix_message=pending_auction_dma_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Auction child order')

        new_auction_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_auction_dma_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Auction child order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_auction_order = FixMessageOrderCancelRequest(self.pov_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_2)
        # endregion

        time.sleep(2)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion
        
        self.fix_verifier_buy.set_case_id(self.case_id_3)
        cancel_dma_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Auction DMA 1 child')

        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')