import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_cases.algo.Algo_TWAP.QAP_T4655 import ToQuod
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, Reference, OrderType, TimeInForce
from datetime import datetime, timedelta
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager

class QAP_T4673(TestCase):
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
        self.order_type = OrderType.Limit.value
        self.tif_day = TimeInForce.Day.value
        self.tif_ioc = TimeInForce.ImmediateOrCancel.value

        self.price_ask = 40
        self.qty_ask = 100_000

        self.price_bid = 30
        self.qty_bid = 100_000

        self.last_trade_qty = 0
        self.last_trade_price = 0

        self.qty = 1_000_000
        self.price = 130
        self.waves = 5

        self.child_qty = AFM.get_next_twap_slice(self.qty, self.waves)
        self.child_traded_qty = 50_000
        self.price_child = 29.99
        self.price_child_neutral = 35
        self.trade_delay = 0
        # endregion

        # region Venue params
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')
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
        self.status_replaces = Status.CancelReplace
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Start/EndDate for algo
        utcnow = datetime.utcnow()
        end_date = (utcnow + timedelta(minutes=self.waves)).strftime("%Y%m%d-%H:%M:%S")
        start_date = utcnow.strftime("%Y%m%d-%H:%M:%S")
        # endregion

        # region EndDate for TradingPhases
        now = datetime.now()
        end_date_open = now + timedelta(minutes=self.waves)
        # endregion

        # region rules
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child, self.price_child, self.child_qty, self.child_traded_qty, self.trade_delay)
        ocrr_rule = rule_manager.add_OCRR(self.fix_env1.buy_side)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, nos_trade_rule, ocrr_rule, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
        trading_phases = AFM.update_endtime_for_trading_phase_by_phase_name(trading_phases, TradingPhases.Open, end_date_open)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(5)
        # endregion

        # region send trading phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create TWAP Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Redburn_params()
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.twap_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, StartDate2=start_date, EndDate2=end_date))

        self.fix_manager_sell.send_message_and_receive_response(self.twap_order, self.case_id_1)

        time.sleep(5)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.twap_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check TWAP child
        self.case_id_2 = bca.create_event("TWAP DMA child order 1", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_2)

        self.twap_child_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.twap_child_1.change_parameters(dict(OrderQty=self.child_qty, Price=self.price_child, Account=self.account, ExDestination=self.ex_destination_1, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.twap_child_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle TWAP child 1')

        pending_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_twap_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP child 1')

        new_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_twap_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP child 1')
        
        partial_fill_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child_1, self.gateway_side_buy, self.status_partial_fill)
        self.fix_verifier_buy.check_fix_message(partial_fill_twap_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Partial Fill TWAP child 1')

        time.sleep(40)

        neutral_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child_1, self.gateway_side_buy, self.status_replaces)
        neutral_twap_child_1_params.change_parameters(dict(Price=self.price_child_neutral))
        self.fix_verifier_buy.check_fix_message(neutral_twap_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Neutral TWAP child 1')
    # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order
        self.case_id_cancel = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_cancel)

        cancel_request_twap_order = FixMessageOrderCancelRequest(self.twap_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_order, self.case_id_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_request_twap_order, direction=ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        self.fix_verifier_buy.set_case_id(self.case_id_cancel)
        cancel_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_twap_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel TWAP child 1')

        cancel_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_twap_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion

