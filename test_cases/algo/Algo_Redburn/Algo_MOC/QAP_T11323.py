import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.data_sets.constants import TradingPhases, Reference, FreeNotesReject
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TimeInForce
from datetime import datetime, timedelta
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T11323(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        # endregion

        # region Market data params
        self.price_ask = 35
        self.qty_ask = 1000000

        self.price_bid = 0
        self.qty_bid = 0
        # endregion

        self.close_px = 35
        self.close_qty = 10000

        self.tif_atc = constants.TimeInForce.AtTheClose.value
        self.free_notes = FreeNotesReject.ReachedMaximumNumberOfUnsuccessfulAtLastAttempts.value

        # order params
        self.qty = 1_000_000
        self.price = 35

        self.percentage_volume = 10

        self.qty_tal_child = self.qty
        self.price_tal_child = self.price

        self.check_order_sequence = True
        # endregion

        # region Venue params
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
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
        self.status_reject = Status.Reject
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        self.rule_list = []

        # region pre-filters
        self.pre_fileter_35_D = self.data_set.get_pre_filter('pre_filer_equal_D')
        self.pre_fileter_35_8_Pending_new = self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new')
        self.pre_fileter_35_8_New = self.data_set.get_pre_filter('pre_filer_equal_ER_new')
        self.pre_fileter_35_8_Fill = self.data_set.get_pre_filter('pre_filer_equal_ER_fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region rules
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.close_px)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.AtLast, TimeSlot.current_phase)
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region send trading phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.close_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.close_px).set_phase(TradingPhases.AtLast)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_close_px().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.close_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.close_px).set_phase(TradingPhases.AtLast)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.auction_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOC_AtLast_params()
        self.auction_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.auction_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume))

        self.fix_manager_sell.send_message_and_receive_response(self.auction_order, self.case_id_1)
        # endregion
        time.sleep(5)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.auction_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle', )

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_order, self.gateway_side_sell, self.status_pending)
        pending_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc))
        self.fix_verifier_sell.check_fix_message(pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_order, self.gateway_side_sell, self.status_new)
        new_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc))
        self.fix_verifier_sell.check_fix_message(new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion
        
        time.sleep(20)
        
        # region Check POV child
        # region Check Would child orders in sequence
        self.case_id_2 = bca.create_event("POV TAL child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_2)

        auction_tal_child = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        auction_tal_child.change_parameters(dict(OrderQty=self.qty_tal_child, Price=self.price_tal_child, Account=self.account, Instrument='*', ExDestination=self.ex_destination_1))

        pending_auction_tal_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(auction_tal_child, self.gateway_side_buy, self.status_pending)

        new_auction_tal_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(auction_tal_child, self.gateway_side_buy, self.status_new)

        cancel_auction_tal_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(auction_tal_child, self.gateway_side_buy, self.status_cancel)

        self.fix_verifier_buy.check_fix_message_sequence([auction_tal_child, auction_tal_child, auction_tal_child, auction_tal_child, auction_tal_child], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.check_fix_message_sequence([pending_auction_tal_child_params, pending_auction_tal_child_params, pending_auction_tal_child_params, pending_auction_tal_child_params, pending_auction_tal_child_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.check_fix_message_sequence([new_auction_tal_child_params, new_auction_tal_child_params, new_auction_tal_child_params, new_auction_tal_child_params, new_auction_tal_child_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.check_fix_message_sequence([cancel_auction_tal_child_params, cancel_auction_tal_child_params, cancel_auction_tal_child_params, cancel_auction_tal_child_params, cancel_auction_tal_child_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order
        case_id_2 = bca.create_event("Eliminate Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        time.sleep(3)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        eliminate_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_order, self.gateway_side_sell, self.status_eliminate)
        eliminate_auction_order_params.change_parameters(dict(Text=self.free_notes, TimeInForce=self.tif_atc))
        self.fix_verifier_sell.check_fix_message(eliminate_auction_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Eliminate')
        # endregion

