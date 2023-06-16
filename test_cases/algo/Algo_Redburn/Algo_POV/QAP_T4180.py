import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, Rounding
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
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T4180(TestCase):
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

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 100

        self.qty_bid_par = 7000
        self.qty_bid_trqx = 5500

        self.percentage_volume = 10

        self.qty = 1000
        self.price = 130

        self.price_ltq = 0
        self.qty_ltq_1 = 0

        self.round_floor = Rounding.Floor.value

        self.passive_xpar_pov_qty_1 = self.passive_trqx_pov_qty_1 = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)
        self.passive_xpar_pov_qty_2 = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid_par, self.qty, self.round_floor)
        self.passive_trqx_pov_qty_2 = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid_trqx, self.qty - self.passive_xpar_pov_qty_2, self.round_floor)

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
        self.status_cancel_replace = Status.CancelReplace
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_5")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_xpar = self.data_set.get_account_by_name("account_2")
        self.account_trqx = self.data_set.get_account_by_name("account_5")
        self.s_par = self.data_set.get_listing_id_by_name("listing_2")
        self.s_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_5")
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_8_Cancel_Replace = self.data_set.get_pre_filter('pre_filer_equal_ER_cancel_replace')
        self.pre_fileter_35_8_Eliminate = self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule_xpar_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price_bid)
        nos_rule_trqx_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price_bid)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule_xpar_1, nos_rule_trqx_1, ocrr_rule, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Send MarketData on XPAR
        case_id_0 = bca.create_event("Send MarketData", self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on PARIS", case_id_0))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        # region Send MarketData on TRQX
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on TURQUOISE", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on TURQUOISE", case_id_0))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(2)
        # endregion

        # region Fix verifier buy
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Redburn_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume))
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, case_id_1)

        time.sleep(10)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.pov_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        new_pov_order_params.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Create list of fix message for check_message_sequence
        # region Passive XPAR order
        passive_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.passive_xpar_pov_qty_1, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_new)
        # endregion

        # region Passive TRQX order
        passive_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.passive_xpar_pov_qty_1, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_trqx))

        pending_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_new)
        # endregion
        # endregion

        # region Check the first 2 passive POV SOR child orders
        self.case_id_2 = bca.create_event("Check 2 Passive POV SOR child order", self.test_id)
        case_id_3 = bca.create_event("Check NewOrderSingle, PendingNew, New of POV SOR child order", self.case_id_2)
        self.fix_verifier_buy.set_case_id(case_id_3)
        
        self.fix_verifier_buy.check_fix_message_sequence(fix_messages_list=[passive_child_order_par_1, passive_child_order_trqx_1], key_parameters_list=[self.key_params, self.key_params], direction=self.FromQuod, pre_filter=self.pre_fileter_35_D, check_order=self.check_order_sequence, message_name='Check NewOrderSingle PAR and TRQX Passive POV child orders')

        self.fix_verifier_buy.check_fix_message_sequence(fix_messages_list=[pending_passive_child_order_par_1_params, pending_passive_child_order_trqx_1_params], key_parameters_list=[self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Pending_new, check_order=self.check_order_sequence, message_name='Check ExecReport PendingNew PAR and TRQX Passive POV child orders')

        self.fix_verifier_buy.check_fix_message_sequence(fix_messages_list=[new_passive_child_order_par_1_params, new_passive_child_order_trqx_1_params], key_parameters_list=[self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_New, check_order=self.check_order_sequence, message_name='Check ExecReport New PAR and TRQX Passive POV child orders')
        # endregion

        # region Send MarketData to trigger the POV SOR Passive order creation
        case_id_4 = bca.create_event("Send MarketData to trigger the new passive child order generation", self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_4))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid_par)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(2)

        # region Send MarketData on TRQX
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on TURQUOISE", case_id_4))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid_trqx)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        
        time.sleep(2)
        
        # region Create list of fix message for check_message_sequence
        # region modified Passive XPAR order
        self.modified_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_cancel_replace)
        self.modified_passive_child_order_par_1_params.change_parameters(dict(OrderQty=self.passive_xpar_pov_qty_2))
        # endregion

        # region modified Passive TRQX order
        self.modified_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_cancel_replace)
        self.modified_passive_child_order_trqx_1_params.change_parameters(dict(OrderQty=self.passive_trqx_pov_qty_2))
        # endregion
        # endregion

        # region Check that 2 passive pov child orders have correct modified qty
        case_id_5 = bca.create_event("Check that POV SOR Passive child orders has correct qty after L1 MarketData is changed", self.case_id_2)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.fix_verifier_buy.check_fix_message_sequence(fix_messages_list=[self.modified_passive_child_order_par_1_params, self.modified_passive_child_order_trqx_1_params], key_parameters_list=[self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Cancel_Replace, check_order=self.check_order_sequence, message_name='Check ExecReport CancelReplace PAR and TRQX Passive POV child orders')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_6 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_6)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_6)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Cancel passive POV child orders 
        case_id_7 = bca.create_event("Cancel POV Child Orders", self.case_id_2)
        self.fix_verifier_buy.set_case_id(case_id_7)
        
        cancel_dma_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.modified_passive_child_order_par_1_params, self.gateway_side_buy, self.status_cancel)
        cancel_dma_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.modified_passive_child_order_trqx_1_params, self.gateway_side_buy, self.status_cancel)
        
        self.fix_verifier_buy.check_fix_message_sequence([cancel_dma_child_1_params, cancel_dma_child_2_params], [self.key_params, self.key_params], direction=self.ToQuod, pre_filter=self.pre_fileter_35_8_Eliminate, check_order=self.check_order_sequence, message_name='Check ExecReport Cancel for PAR and TRQX POV DMA child orders')
        # endregion

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        cancel_pov_order.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion