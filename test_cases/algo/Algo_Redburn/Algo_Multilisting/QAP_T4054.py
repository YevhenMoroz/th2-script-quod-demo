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


class QAP_T4054(TestCase):
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
        self.price_ask_2 = 45
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.qty = 1_000_000
        self.price = 41

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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule_xpar = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, False, 0, self.price_ask)
        nos_ioc_rule_trqx = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, False, 0, self.price)
        nos_ioc_rule_trqx_2 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, False, 0, self.price_ask)
        nos_passive_rule_xpar = rule_manager.add_NOS(self.fix_env1.buy_side, account=self.account_xpar)
        ocr_rule_xpar = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_ioc_rule_xpar, nos_ioc_rule_trqx, nos_ioc_rule_trqx_2, nos_passive_rule_xpar, ocr_rule_xpar]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send MarketData on XPAR
        case_id_0 = bca.create_event("Send MarketData", self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on PARIS", case_id_0))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
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
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Fix verifier buy
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_RB_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        # endregion

        # region Send market data on Paris and TRQX to prevent generation many IOC orders
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on TURQUOISE", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.multilisting_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        new_multilisting_order_params.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(new_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Aggressive XPAR order
        ioc_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.qty, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Aggressive Child DMA order')

        new_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Aggressive Child DMA order')

        eliminate_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_eliminated)
        self.fix_verifier_buy.check_fix_message(eliminate_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate Aggressive Child DMA 2 order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order

        case_id_5 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_5)
        # endregion

        cancel_request_multilisting_order = FixMessageOrderCancelRequest(self.multilisting_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_multilisting_order, case_id_5)
        self.fix_verifier_sell.check_fix_message(cancel_request_multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region check cancellation parent POV order
        cancel_multilisting_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_cancel)
        cancel_multilisting_order.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(cancel_multilisting_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion