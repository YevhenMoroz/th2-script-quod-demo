import os
import sched
import time
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, FreeNotesReject
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T10429(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 componentsMACHINE GUN KELLY
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        # endregion

        # region order parameters
        self.qty = 1000
        self.waves = 5
        self.percentage = 100
        self.price = 130
        self.price_bbid = 30
        self.price_bask = 40
        self.ltp_price = 100
        self.child_price = AFM.calc_ticks_offset_minus(self.price_bbid, 1, 0.005)
        self.historical_volume = 1000.0

        self.tif_atc = TimeInForce.AtTheClose.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
        self.status_reject = Status.Reject
        self.status_fill = Status.Fill
        # endregion

        self.free_notes = FreeNotesReject.CouldNotRetrieveAverageVolumeDistribution.value

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_3")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_D_multilisted = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_D_multilisted['Price'] = (self.price_bask, "EQUAL")
        self.pre_fileter_35_D_passive = deepcopy(self.data_set.get_pre_filter('pre_filer_equal_D'))
        self.pre_fileter_35_D_passive['Price'] = (self.child_price, "EQUAL")
        self.pre_fileter_35_D_neutral = deepcopy(self.data_set.get_pre_filter('pre_filer_equal_D'))
        self.pre_fileter_35_D_neutral['Price'] = (self.price_bbid, "EQUAL")

        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_8_Fill = self.data_set.get_pre_filter('pre_filer_equal_ER_fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.price_bbid)
        nos_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.child_price)
        ocrr1 = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.mic, True, 0)
        ioc = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.mic, False, 0, 40, 0)
        ocr = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos, nos_2, ocrr1, ioc, ocr]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open, TimeSlot.current_phase, 15)
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region insert data into mongoDB
        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.listing_id}")
        bca.create_event(f"Collection Q{self.listing_id} is inserted", self.test_id, body=''.join([f"{volume['LastTradedTime']} - {volume['LastTradedQty']}, phase - {volume['LastAuctionPhase']}\n" for volume in curve]))
        # endregion

        self.start_date = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.start_date = self.start_date - timedelta(seconds=self.start_date.second, microseconds=self.start_date.microsecond) + timedelta(minutes=1)
        self.end_date = (self.start_date + timedelta(minutes=5))

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send MarketData", self.test_id))

        self.snapshot_full_refresh_empty = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data_empty()\
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        self.snapshot_full_refresh = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data(self.price_bbid, self.price_bask)\
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler)

        self.fix_manager_feed_handler.send_message(fix_message=self.snapshot_full_refresh_empty)

        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq() \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.ltp_price) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler) \
            .set_phase(TradingPhases.Open)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        case_id_1 = bca.create_event("Create VWAP Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Send VWAP algo
        self.vwap_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_VWAP_buy_back_params()
        self.vwap_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.vwap_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.vwap_algo.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, StartDate2=self.start_date.strftime("%Y%m%d-%H:%M:%S"), EndDate2=self.end_date.strftime("%Y%m%d-%H:%M:%S")))
        self.fix_manager_sell.send_message_and_receive_response(fix_message=self.vwap_algo, case_id=case_id_1)
        # endregion



        # region Check Sell side
        self.auction_algo_verification = deepcopy(self.vwap_algo)
        self.fix_verifier_sell.check_fix_message(fix_message=self.auction_algo_verification, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_algo, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(fix_message=er_pending_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_algo, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(fix_message=er_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion


        # region check sell side
        self.vwap_child = AFM.get_vwap_childs(curve, self.start_date, self.end_date, self.qty)

        dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        dma_order.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.vwap_child[0], Price=self.price_bbid, Instrument=self.instrument))
        dma_order.change_parameter('TransactTime', f'>{self.start_date.isoformat()[:-6]}')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_pending)

        er_new_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_new)

        cancel_dma = FixMessageOrderCancelRequest(dma_order).change_parameters(dict(OrderQty=self.vwap_child[0], Instrument='*', OrderID='*'))
        er_cancel_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_cancel)


        list_multilisted_childs = []
        for i in range(0,6):
            temp_message = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
            temp_message.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.vwap_child[0], Price=self.price_bask, Instrument=self.instrument, TimeInForce=3))
            temp_message.change_parameter('TransactTime', f'<{(self.start_date + timedelta(seconds=41 + i)).isoformat()[:-6]}')

            list_multilisted_childs.append(temp_message)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check child order", self.test_id))

        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enterabs(self.start_date.timestamp() + 25, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(
            fix_message=self.snapshot_full_refresh))
        scheduler.enterabs(self.start_date.timestamp() + 66, 1, self.fix_verifier_buy.check_no_message_found, kwargs=dict(
            message_timeout=60000,
            direction=self.FromQuod,
            pre_filter=self.pre_fileter_35_D_passive,
            message_name="Buy side check that there is no passive child on first slice"))
        scheduler.enterabs(self.start_date.timestamp() + 66, 1, self.fix_verifier_buy.check_no_message_found, kwargs=dict(
            message_timeout=60000,
            direction=self.FromQuod,
            pre_filter=self.pre_fileter_35_D_neutral,
            message_name="Buy side check that there is no neutral child on first slice"))
        scheduler.enterabs(self.start_date.timestamp() + 66, 1, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(
            fix_messages_list=list_multilisted_childs,
            key_parameters_list=[self.key_params,self.key_params,self.key_params,self.key_params,self.key_params,self.key_params],
            direction=self.FromQuod,
            pre_filter=self.pre_fileter_35_D_multilisted,
            message_name="Buy side check multilisted child"))

        scheduler.run()

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Check that algo is Canceled", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        time.sleep(2)

        cancel_request_vwap_order = FixMessageOrderCancelRequest(self.vwap_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_vwap_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_vwap_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(5)

        # region check cancellation parent VWAP order
        cancel_vwap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_algo, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_vwap_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region
