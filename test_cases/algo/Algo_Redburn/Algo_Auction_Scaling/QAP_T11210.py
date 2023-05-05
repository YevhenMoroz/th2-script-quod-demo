import os
import sched
import time

from pathlib import Path
from datetime import datetime, timedelta

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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.db_wrapper.db_manager import DBManager


class QAP_T11210(TestCase):
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
        self.qty = 10000
        self.price = 120
        self.indicative_volume = 10000
        self.indicative_volume_new = 5000
        self.indicative_price = 120
        self.percentage_volume = 10

        self.pp1_percentage = 11
        self.pp1_price = 120
        self.pp2_percentage = 12
        self.pp2_price = 119

        self.scaling_child_order_qty = '%^(1[2-4]|1236)$'  # fisrt number 111112, 23-37K and any 3 number
        self.scaling_child_order_modified_qty = '%^([4-5]|466)$'  # fisrt number 111112, 23-37K and any 3 number
        self.scaling_child_order_price = '%^1(20|19.[1-9]|19)$'  # the first number 130, 120, 117 or 119.7-117.3 with step 3

        self.check_order_sequence = False

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

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_G = self.data_set.get_pre_filter('pre_filer_equal_G')
        self.pre_fileter_35_8_CancelReplace = self.data_set.get_pre_filter('pre_filer_equal_ER_cancel_replace')
        self.pre_fileter_35_8_Eliminate = self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate')
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportAll(self.fix_env1.buy_side, self.account, self.ex_destination_1, 30000)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1)
        self.rule_list = [nos_rule, ocr_rule, ocrr_rule]
        # endregion

        # region EndDate for TradingPhases
        now = datetime.now()
        end_date_pre_close = now + timedelta(minutes=2)
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
        trading_phases = AFM.update_endtime_for_trading_phase_by_phase_name(trading_phases, TradingPhases.PreClosed, end_date_pre_close)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Mongo insert
        self.db_manager.create_empty_collection(collection_name=f"Q{self.listing_id}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price).set_phase(TradingPhases.PreClosed)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        initial_slice = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False) - 65
        end_time_minus_1_min = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False) - 62
        end_time_minus_54_sec = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False) - 50
        end_time_minus_25_sec = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False) - 20
        end_time = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False) + 5

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOC_Scaling_params()
        self.auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.auction_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, PricePoint1Price=self.pp1_price, PricePoint1Participation=self.pp1_percentage, PricePoint2Price=self.pp2_price, PricePoint2Participation=self.pp2_percentage))
        scheduler.enterabs(initial_slice, 1, self.fix_manager_sell.send_message_and_receive_response, kwargs=dict(fix_message=self.auction_algo))

        # region Check Sell side
        self.case_id_2 = bca.create_event("Scaling child orders", self.test_id)

        scheduler.enterabs(initial_slice, 1,  self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=self.auction_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle'))

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_pending)
        pending_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc))
        scheduler.enterabs(initial_slice, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew'))

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_new)
        new_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc))
        scheduler.enterabs(initial_slice, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New'))
        # endregion

        # region Scaling child orders
        scaling_dma_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.scaling_child_order_price, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order, self.gateway_side_buy, self.status_new)

        # region Check that the child DMA order is replaced
        cancel_replace_scaling_dma_child_order_params = FixMessageOrderCancelReplaceRequestAlgo(scaling_dma_child_order)
        cancel_replace_scaling_dma_child_order_params.change_parameters(dict(OrderQty=self.scaling_child_order_modified_qty, QtyType='0'))

        er_cancel_replace_scaling_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order, self.gateway_side_buy, self.status_cancel_replace)
        er_cancel_replace_scaling_dma_child_order_params.change_parameters(dict(OrderQty=self.scaling_child_order_modified_qty))
        # endregion

        self.cancel_scaling_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(er_cancel_replace_scaling_dma_child_order_params, self.gateway_side_buy, self.status_cancel)
        # endregion

        # region Check 35=D of child orders
        scheduler.enterabs(end_time_minus_1_min, 1, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.FromQuod, pre_filter=self.pre_fileter_35_D, check_order=self.check_order_sequence))
        # endregion

        # region Send new Indicative volume 5000
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Decrease Indicative volume", self.test_id))
        self.incremental_refresh_1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume_new).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price).set_phase(TradingPhases.PreClosed)
        scheduler.enterabs(end_time_minus_1_min, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_1))
        # endregion

        # region Check 35=D of child orders
        scheduler.enterabs(end_time_minus_54_sec, 1, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order, scaling_dma_child_order], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.FromQuod, pre_filter=self.pre_fileter_35_D, check_order=self.check_order_sequence))
        # endregion

        # region Check Pending New and New execution report for child orders
        scheduler.enterabs(end_time_minus_25_sec, 1, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params, pending_scaling_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Pending_new, check_order=self.check_order_sequence))

        scheduler.enterabs(end_time_minus_25_sec, 2, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params, new_scaling_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_New, check_order=self.check_order_sequence))

        scheduler.enterabs(end_time_minus_25_sec, 2, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params, cancel_replace_scaling_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], pre_filter=self.pre_fileter_35_G, check_order=self.check_order_sequence))
        # endregion

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 11 Scaling child orders Buy Side NewOrderSingle, Pending New and New, CancelReplace", self.case_id_2))
        scheduler.enterabs(end_time_minus_25_sec, 2, self.fix_verifier_buy.check_fix_message_sequence, kwargs=dict(fix_messages_list=[er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params, er_cancel_replace_scaling_dma_child_order_params], key_parameters_list=[self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_CancelReplace, check_order=self.check_order_sequence))
        # endregion

        scheduler.run()


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_4 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)

        cancel_request_auction_order = FixMessageOrderCancelRequest(self.auction_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_auction_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(5)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Check cancellation of the Scaling child orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 11 Scaling child orders Buy Side Cancel", case_id_4))
        self.fix_verifier_buy.check_fix_message_sequence([self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params, self.cancel_scaling_child_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.pre_fileter_35_8_Eliminate, check_order=self.check_order_sequence)
        # endregion

        # region check cancellation parent Auction order
        cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_cancel)
        cancel_auction_order.change_parameters(dict(TimeInForce=self.tif_atc))
        self.fix_verifier_sell.check_fix_message(cancel_auction_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion