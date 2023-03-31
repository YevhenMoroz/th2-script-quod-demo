import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, Reference
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T4643(TestCase):
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

        self.order_type = constants.OrderType.Limit.value
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_reactive = constants.TimeInForce.ImmediateOrCancel.value

        self.price_ask = 30
        self.qty_ask = 200

        self.price_bid = 20
        self.qty_bid = 200

        self.percentage_volume = 10

        self.last_trade_price = 20
        self.last_trade_qty = 100
        self.day_highest = 25.0
        # endregion

        # order params
        self.qty = 300
        self.price = 30
        self.qty_child_passive = 23
        self.price_child_passive = 20
        self.qty_child_aggressive = 12
        self.price_child_aggressive = 24.995
        self.aggressivity = constants.Aggressivity.Passive.value
        # endregion

        # region Algo params
        self.passive_reference_price = Reference.Market.value
        self.passive_offset = 0
        self.limit_price_reference = Reference.DayHight.value
        self.limit_price_offset = 1
        # endregion

        # region Venue params
        # self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        # self.client = self.data_set.get_client_by_name("client_2")
        # self.account = self.data_set.get_account_by_name('account_2')
        # self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_38")
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_21")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_47")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_58")
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
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        self.status_eliminate = Status.Eliminate
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        self.rule_list = []

        # # region SSH
        # self.config_file = "client_sats.xml"
        # self.xpath = ".//bpsOffsets"
        # self.new_config_value = 'false'
        # self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        # self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user, self.ssh_client_env.password, self.ssh_client_env.su_user, self.ssh_client_env.su_password)
        # self.default_config_value = self.ssh_client.get_and_update_file(self.config_file, {self.xpath: self.new_config_value})
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # # region precondition: Prepare SATS configuration
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # # endregion

        # region rules
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child_passive)
        reactive_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child_aggressive)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, ocr_rule, reactive_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
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
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region send highPX
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_high_px().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.day_highest)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Redburn_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(LimitPriceReference=self.limit_price_reference, LimitPriceOffset=self.limit_price_offset, Passive=self.passive_reference_price, PassiveOffset=self.passive_offset, MaxPercentageVolume=self.percentage_volume, Aggressivity=self.aggressivity))

        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, self.case_id_1)
        # endregion
        time.sleep(5)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.pov_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check Anticipative  child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Check Anticipative child order", self.test_id))

        self.anticipative_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.anticipative_child_order.change_parameters(dict(Account=self.account, OrderQty=self.qty_child_passive, Price=self.price_child_passive, Instrument='*', ExDestination=self.ex_destination_1))
        self.fix_verifier_buy.check_fix_message(self.anticipative_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Anticipative Child')

        pending_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.anticipative_child_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  Anticipative Child')

        new_vwap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.anticipative_child_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_vwap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New pov child')
        # endregion

        # region Check Reactive child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Reactive child order", self.test_id))

        reactive_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        reactive_child_order.change_parameters(dict(Account=self.account, OrderQty=self.qty_child_aggressive, Price=self.price_child_aggressive, Instrument='*', ExDestination=self.ex_destination_1))
        self.fix_verifier_buy.check_fix_message(reactive_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Reactive Child')

        pending_reactive_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(reactive_child_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_reactive_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  Reactive Child')

        new_reactive_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(reactive_child_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_reactive_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  Reactive Child')

        eliminate_reactive_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(reactive_child_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(eliminate_reactive_child_order_2, self.key_params, self.ToQuod, "Buy Side ExecReport Reactive Child")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order
        self.case_id_cancel = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_cancel)

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, self.case_id_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # # region config reset
        # self.default_config_value = self.ssh_client.get_and_update_file(self.config_file, {self.xpath: self.new_config_value})
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # self.ssh_client.close()
        # # endregion

        self.fix_verifier_buy.set_case_id(self.case_id_cancel)
        cancel_pov_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.anticipative_child_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_pov_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel pov child')

        cancel_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion
