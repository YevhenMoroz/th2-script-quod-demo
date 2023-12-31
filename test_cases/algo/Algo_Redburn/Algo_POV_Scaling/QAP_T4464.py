import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, OrderSide, TradingPhases
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T4464(TestCase):
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
        self.order_type = constants.OrderType.Limit.value
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value

        self.price_ask = 130
        self.qty_ask = 100_000

        self.price_bid = 110
        self.qty_bid = 100_000

        self.ltp = 100
        self.ltq = 100_000

        self.percentage_volume = 10
        self.pp1_offset = -200
        self.pp1_reference = constants.Reference.LastTradePrice.value
        self.pp1_participation = 20
        self.pp2_offset = 250
        self.pp2_reference = constants.Reference.LastTradePrice.value
        self.pp2_participation = 40
        self.number_of_levels = 10

        self.pp1_price_with_reference_and_offset = AFM.calc_bps_offset_minus(self.ltp, self.pp1_offset * (-1))  #98
        self.pp2_price_with_reference_and_offset = AFM.calc_bps_offset_plus(self.ltp, self.pp2_offset)          #102.5
        self.step = AFM.calc_step_for_scaling(self.pp2_price_with_reference_and_offset, self.pp1_price_with_reference_and_offset, self.number_of_levels)    #0.45

        self.level_1_price = round(self.pp1_price_with_reference_and_offset + self.step, 2)
        self.level_2_price = round(self.level_1_price + self.step, 2)
        self.level_3_price = round(self.level_2_price + self.step, 2)
        self.level_4_price = round(self.level_3_price + self.step, 2)
        self.level_5_price = round(self.level_4_price + self.step, 2)
        self.level_6_price = round(self.level_5_price + self.step, 2)
        self.level_7_price = round(self.level_6_price + self.step, 2)
        self.level_8_price = round(self.level_7_price + self.step, 2)
        self.level_9_price = round(self.level_8_price + self.step, 2)

        self.qty = 1_000_000
        self.price = 95

        self.scaling_child_order_qty = '%^(1[1-3]|[2-5])\d{3}$'  # fisrt number 11-12 or 7-9 and any 3 number
        self.scaling_child_order_price = '%^(9|10)(0|[1-2,5,8-9]|[0-2,8,9].\d{1,2})$'  # the first number 95, 98-102.any 1-2 number

        self.qty_passive_child_1 = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)

        self.side_sell = OrderSide.Sell.value

        self.check_order_sequence = False
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        self.status_eliminated = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_36")
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_ask)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.price)
        nos_ioc_rule_1 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.pp1_price_with_reference_and_offset)
        nos_ioc_rule_2 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_1_price)
        nos_ioc_rule_3 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_2_price)
        nos_ioc_rule_4 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_3_price)
        nos_ioc_rule_5 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_4_price)
        nos_ioc_rule_6 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_5_price)
        nos_ioc_rule_7 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_6_price)
        nos_ioc_rule_8 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_7_price)
        nos_ioc_rule_9 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_8_price)
        nos_ioc_rule_10 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.level_9_price)
        nos_ioc_rule_11 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.pp2_price_with_reference_and_offset)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, nos_ioc_rule, nos_ioc_rule_1, nos_ioc_rule_2, nos_ioc_rule_3, nos_ioc_rule_4, nos_ioc_rule_5, nos_ioc_rule_6, nos_ioc_rule_7, nos_ioc_rule_8, nos_ioc_rule_9, nos_ioc_rule_10, nos_ioc_rule_11, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.ltp, MDEntrySize=self.ltq)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Scaling_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, Side=self.side_sell))
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, PricePoint1Offset=self.pp1_offset, PricePoint1Reference=self.pp1_reference, PricePoint1Participation=self.pp1_participation, PricePoint2Offset=self.pp2_offset, PricePoint2Reference=self.pp2_reference, PricePoint2Participation=self.pp2_participation))
        self.pov_order.remove_fields_from_component('QuodFlatParameters', ['PricePoint1Price', 'PricePoint2Price'])
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, case_id_1)

        time.sleep(10)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.pov_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check passive child order 1
        case_id_2 = bca.create_event("Scaling child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy side NewOrderSingle", case_id_2))

        # region Aggressive Scaling order
        scaling_ioc_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_ioc_child_order.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.scaling_child_order_price, TimeInForce=self.tif_ioc, Instrument='*', Side=self.side_sell))

        pending_scaling_ioc_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_ioc_child_order, self.gateway_side_buy, self.status_pending)

        new_scaling_ioc_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_ioc_child_order, self.gateway_side_buy, self.status_new)

        eliminate_scaling_ioc_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_ioc_child_order, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check Scaling child orders
        self.fix_verifier_buy.check_fix_message_sequence([scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order, scaling_ioc_child_order], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side Pending New", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params, pending_scaling_ioc_child_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side New", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params, new_scaling_ioc_child_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side Eliminate Aggressive", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params, eliminate_scaling_ioc_child_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion
