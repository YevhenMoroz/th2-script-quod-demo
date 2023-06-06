import os
import sched
import time
from datetime import datetime, timedelta, timezone

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


class QAP_T4172(TestCase):
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
        self.indicative_volume = 1000
        self.historical_volume = 1000.0

        self.qty = 1_000_000
        self.price = 40
        self.max_part = 10
        self.scal_opt = False

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.ltq = 1000
        self.ltp = 1

        self.slice_qty = AFM.get_twap_child_qty_with_min_max_participation(self.max_part, self.ltq, self.qty)
        self.auction_child_qty = AFM.get_child_qty_for_auction(self.indicative_volume, self.max_part, self.qty)

        # Because of the bi-lateral behaviour the 1st auc child changed qty to 99. And the new child with the qty=1 is created
        self.cancel_auc_qty_1 = 99
        self.cancel_auc_qty_2 = 1

        self.passive_phase_price = self.price_bid - 0.005
        self.neutral_phase_price = int((self.price_bid + self.price_ask) / 2)

        self.tif_ato = TimeInForce.AtTheOpening.value
        self.tif_ioc = TimeInForce.ImmediateOrCancel.value
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

        # region Venue params
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        # endregion

        # region Key parameters
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.passive_phase_price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, nos_rule2, ocrr_rule, ocr_rule]
        # endregion

        self.send_algo = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.send_algo = self.send_algo - timedelta(seconds=self.send_algo.second, microseconds=self.send_algo.microsecond) + timedelta(minutes=1)
        self.end_phase = (self.send_algo + timedelta(minutes=1))
        start_date = self.send_algo.strftime("%Y%m%d-%H:%M:%S")

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.PreOpen)
        trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.PreOpen, self.end_phase)
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region insert data into mongoDB
        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.listing_id}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion

        # region Send MarketData for the TWAP order
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_ind_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).set_phase(TradingPhases.PreOpen)
        self.fix_manager_feed_handler.send_message(market_data_incremental_ind_par)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        send_algo_order_checkpoint = self.end_phase.timestamp() - 60
        auction_child_checkpoint = self.end_phase.timestamp() - 50
        send_incremental_refresh_opn_checkpoint = self.end_phase.timestamp() + 1
        send_incremental_refresh_ltq_checkpoint = self.end_phase.timestamp() + 10

        # region Send NewOrderSingle (35=D) for
        case_id_1 = bca.create_event("Create TWAP Order", self.test_id)
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_manager_sell.set_case_id, kwargs=dict(case_id=case_id_1))

        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_auction_params()
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_xpar))
        self.twap_order.update_fields_in_component('QuodFlatParameters', dict(StartDate2=start_date, MaxParticipation=self.max_part))
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.twap_order))

        # region Check Sell side
        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_verifier_sell.set_case_id, kwargs=dict(case_id=case_id_1))

        scheduler.enterabs(send_algo_order_checkpoint, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.twap_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        er_pending_new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        scheduler.enterabs(send_algo_order_checkpoint, 2, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=er_pending_new_twap_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew'))

        er_new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        scheduler.enterabs(send_algo_order_checkpoint, 3, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=er_new_twap_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New'))
        # endregion

        # region Check DMA Auction child order
        self.case_id_2 = bca.create_event("TWAP child order", self.test_id)

        self.dma_auction_child_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.dma_auction_child_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.auction_child_qty, Price=self.price, TimeInForce=self.tif_ato, Instrument=self.instrument))
        scheduler.enterabs(auction_child_checkpoint, 1, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.dma_auction_child_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle DMA Auction child'))

        er_pending_new_dma_auction_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_auction_child_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(auction_child_checkpoint, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_pending_new_dma_auction_child_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Auction child'))

        self.fix_verifier_buy.set_case_id(bca.create_event("Check Auction child order Buy Side NewOrderSingle, Pending New, New", self.case_id_2))

        er_new_dma_auction_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_auction_child_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(auction_child_checkpoint, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_new_dma_auction_child_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Auction child'))
        # endregion

        # region Send Open phase
        case_id_3 = bca.create_event("Send the Open phase", self.test_id)
        scheduler.enterabs(send_incremental_refresh_opn_checkpoint, 1, self.fix_manager_feed_handler.set_case_id, kwargs=dict(case_id=case_id_3))
        
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        self.incremental_refresh_1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        scheduler.enterabs(send_incremental_refresh_opn_checkpoint, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion

        # region Send LTQ
        case_id_4 = bca.create_event("Send LTQ incremental refresh", self.test_id)
        scheduler.enterabs(send_incremental_refresh_ltq_checkpoint, 1, self.fix_manager_feed_handler.set_case_id, kwargs=dict(case_id=case_id_4))
        
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        self.incremental_refresh_1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.ltp, MDEntrySize=self.ltq)
        scheduler.enterabs(send_incremental_refresh_ltq_checkpoint, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion

        scheduler.run()

        time.sleep(65)

        # region Check that the DMA Auction child was cancelled
        self.fix_verifier_buy.set_case_id(self.case_id_2)

        er_cancelled_dma_1_auction_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_auction_child_order, self.gateway_side_buy, self.status_cancel)
        er_cancelled_dma_1_auction_child_order_params.change_parameters(dict(OrderQty=self.cancel_auc_qty_1))
        self.fix_verifier_buy.check_fix_message(er_cancelled_dma_1_auction_child_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancelled DMA 1 Auction child')

        er_cancelled_dma_2_auction_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_auction_child_order, self.gateway_side_buy, self.status_cancel)
        er_cancelled_dma_2_auction_child_order_params.change_parameters(dict(OrderQty=self.cancel_auc_qty_2))
        self.fix_verifier_buy.check_fix_message(er_cancelled_dma_2_auction_child_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancelled DMA 2 Auction child')
        # endregion

        # region Check the 1st TWAP slice order
        self.case_id_3 = bca.create_event("Check the 1st TWAP slice", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_3)

        self.twap_slice_1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.twap_slice_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.slice_qty, Price=self.passive_phase_price, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.twap_slice_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle TWAP slice 1 order')

        er_pending_new_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_twap_slice_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP slice 1 order')

        er_new_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_twap_slice_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP slice 1 order')
        # endregion

        # region Check the 1st replacing of the 1st TWAP slice
        self.fix_verifier_buy.set_case_id(bca.create_event("1st TWAP slice goes to the neutral phase", self.case_id_3))

        self.twap_slice_1_order.change_parameters(dict(Price=self.neutral_phase_price))

        er_replaced_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_1_order, self.gateway_side_buy, self.status_cancel_replace)
        self.fix_verifier_buy.check_fix_message(er_replaced_twap_slice_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side 1st ExecReport Replaced TWAP slice 1 order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        cancel_request_twap_order = FixMessageOrderCancelRequest(self.twap_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_twap_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # endregion

        time.sleep(5)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        # region Revert the TradingPhase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Check ERs Cancelled for the parent TWAP (1st LVL) and the DMA Auction child (3rd LVL)
        self.fix_verifier_buy.set_case_id(self.case_id_3)
        er_cancelled_twap_slice_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_slice_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancelled_twap_slice_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel TWAP slice 1 order')

        er_cancelled_twap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancelled_twap_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion
