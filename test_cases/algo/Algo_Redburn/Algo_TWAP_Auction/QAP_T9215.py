import os
import sched
import time
from datetime import datetime, timedelta

from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce
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



class QAP_T9215(TestCase):
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
        self.indicative_volume = 0
        self.historical_volume = 1000000.0

        self.qty = 1_000_000
        self.price = 40

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.auction_child_qty = self.qty
        self.twap_child = AFM.get_next_twap_slice(self.qty, 6)
        self.twap_child_price = self.price_bid - 0.005

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
        # self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # self.client = self.data_set.get_client_by_name("client_2")
        # self.account = self.data_set.get_account_by_name("account_2")
        # self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        # self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_38")
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_21")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_47")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_58")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile3")

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        # self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.twap_child_price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_bid)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_rule2, ocr_rule, ocrr_rule,  cancel_rule]
        # endregion

        # now = datetime.utcnow() + timedelta(minutes=1) - timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
        # end_date_open = now + timedelta(minutes=5)

        utcnow = datetime.utcnow() + timedelta(minutes=1) - timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
        end_date = (utcnow + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")
        start_date = utcnow.strftime("%Y%m%d-%H:%M:%S")

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open, TimeSlot.current_phase, duration=6)
        # trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.Open, end_date_open)

        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region insert data into mongoDB
        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.listing_id}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion
        
        # region Send MarketData for POV order
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        send_algo_order_checkpoint = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 300
        twap_child_checkpoint = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) - 290
        end_open_phase_checkpoint = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Open, start_time=False) + 1

        # region Send NewOrderSingle (35=D) for
        case_id_1 = bca.create_event("Create TWAP Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.twap_algo_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_auction_params()
        self.twap_algo_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_algo_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.twap_algo_order.update_fields_in_component('QuodFlatParameters', dict(StartDate2=start_date, EndDate2=end_date))
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.twap_algo_order))

        # region Check Sell side
        self.case_id_2 = bca.create_event("TWAP child order", self.test_id)

        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.twap_algo_order, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_algo_order, self.gateway_side_sell, self.status_pending)
        scheduler.enterabs(send_algo_order_checkpoint, 2, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_algo_order, self.gateway_side_sell, self.status_new)
        scheduler.enterabs(send_algo_order_checkpoint, 3, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        # region Check POV child order
        twap_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        twap_child_order.change_parameters(dict(Account=self.account, OrderQty=self.twap_child, Price=self.twap_child_price, Instrument='*', ExDestination=self.ex_destination_1))
        scheduler.enterabs(twap_child_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=twap_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 1'))

        pending_twap_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(twap_child_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_twap_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 1'))

        self.fix_verifier_buy.set_case_id(bca.create_event("Check TWAP child order Buy Side NewOrderSingle, Pending New, New", self.case_id_2))

        new_twap_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(twap_child_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_twap_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 1'))
        # endregion

        # region Send PCL phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send PCL phase", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', 0).set_phase(TradingPhases.PreClosed)
        scheduler.enterabs(end_open_phase_checkpoint, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion
        
        scheduler.run()
        
        time.sleep(5)

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
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_twap_algo_order = FixMessageOrderCancelRequest(self.twap_algo_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_algo_order, case_id_2)
        # endregion

        time.sleep(2)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion
        
        self.fix_verifier_buy.set_case_id(self.case_id_3)
        cancel_dma_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_dma_child_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Auction DMA 1 child')

        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_algo_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')