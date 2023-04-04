import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases
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


class QAP_T10939(TestCase):
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

        self.price_ask = 0
        self.qty_ask = 0
        self.price_ask_1 = 130
        self.qty_ask_1 = 5_000
        self.price_ask_2 = 127

        self.price_bid = 0
        self.qty_bid = 0

        self.percentage_volume = 40
        self.min_participation = 20

        self.qty = 500_000
        self.qty_trade = 1_000
        self.price = 130

        self.price_ltq = 130
        self.qty_ltq_1 = 30_000
        self.qty_ltq_2 = 20_000
        self.executed_aggressive_qty = 1_000

        self.qty_aggressive_child_1 = AFM.get_pov_child_qty_on_ltq(self.percentage_volume, self.qty_ltq_1, self.qty)
        self.qty_aggressive_child_2 = 21434 # qty_aggressive_child_1 + recycling from previous slice

        self.check_order_sequence = True
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
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.executed_aggressive_qty, self.price_ltq)
        nos_ioc_rule_1 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.price_ask_2)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_ioc_rule, nos_ioc_rule_1, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Minimum_Participation_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume, MinParticipation=self.min_participation))
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.pov_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to update the BestAsk", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask_1)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger WorsePrice behavior", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Check IOC child order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("IOC child order - 1", self.test_id))

        ioc_child_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_1.change_parameters(dict(OrderQty=self.qty_aggressive_child_1, Price=self.price_ask_1, Instrument='*', TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(ioc_child_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle IOC Child 1')

        pending_ioc_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  IOC Child 1')

        new_ioc_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_ioc_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  IOC Child 1')

        partial_fill_ioc_child_order_1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_1, self.gateway_side_buy, self.status_partial_fill)
        partial_fill_ioc_child_order_1.change_parameters(dict(OrdType=self.order_type, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(partial_fill_ioc_child_order_1, self.key_params, self.ToQuod, "Buy Side ExecReport Partial Fill IOC Child 1")
        # endregion

        # region Create checkpoint for check POV child order sequence
        self.fix_verifier_buy_2 = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to update the BestAsk", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask_1)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the Price Improvement behavior", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_2)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the Price Improvement behavior", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_2)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        time.sleep(3)
        # region Check that POV generates 2 child order with each other
        case_id_2 = bca.create_event("Check that POV generates 2 child order with each other", self.test_id)
        self.fix_verifier_buy_2.set_case_id(bca.create_event("Create new checkpoint for FIXBUY verifier", case_id_2))

        # region Check IOC child order 2
        ioc_child_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_2.change_parameters(dict(OrderQty=self.qty_ask_1, Price=self.price_ask_2, Instrument='*', TimeInForce=self.tif_ioc))

        pending_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_new)

        eliminated_ioc_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_eliminated)
        eliminated_ioc_child_order_2.change_parameters(dict(OrdType=self.order_type, TimeInForce=self.tif_ioc))
        
        # endregion

        # region Check IOC child order 3
        ioc_child_order_3 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_3.change_parameters(dict(OrderQty=self.qty_aggressive_child_2, Price=self.price_ask_1, Instrument='*', TimeInForce=self.tif_ioc))

        pending_ioc_child_order_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_3, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_3, self.gateway_side_buy, self.status_new)

        eliminated_ioc_child_order_3 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_3, self.gateway_side_buy, self.status_eliminated)
        eliminated_ioc_child_order_3.change_parameters(dict(OrdType=self.order_type, TimeInForce=self.tif_ioc))
        # endregion

        # region Check verifiers sequence
        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 2 POV child order in sequence Buy Side NewOrderSingle", case_id_2))
        self.fix_verifier_buy_2.check_fix_message_sequence([ioc_child_order_2, ioc_child_order_3], [self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 2 POV child order in sequence Buy Side Pending New", case_id_2))
        self.fix_verifier_buy_2.check_fix_message_sequence([pending_ioc_child_order_2_params, pending_ioc_child_order_3_params], [self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 2 POV child order in sequence Buy Side New", case_id_2))
        self.fix_verifier_buy_2.check_fix_message_sequence([new_ioc_child_order_2_params, new_ioc_child_order_3_params], [self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 2 POV child order in sequence Buy Side Eliminate", case_id_2))
        self.fix_verifier_buy_2.check_fix_message_sequence([eliminated_ioc_child_order_2, eliminated_ioc_child_order_3], [self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

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