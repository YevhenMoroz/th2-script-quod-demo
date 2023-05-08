import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.algo_formulas_manager import AlgoFormulasManager


class QAP_T11185(TestCase):
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
        # endregion

        # region order parameters
        self.qty = 400
        self.price = 50
        self.qty_bid_1 = 1000
        self.price_bid_1 = 13
        self.qty_bid_2 = 2000
        self.price_bid_2 = 14
        self.price_ask = 40
        self.qty_ask = 1000
        self.childMinValue = 100
        self.volume = 0.1
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.md_entry_px_incr_r_initial = 0
        self.md_entry_size_incr_r_initial = 0
        self.md_entry_px_incr_r = 40
        self.md_entry_size_incr_r = 700
        self.bool_type = StrategyParameterType.Boolean.value
        self.float_type = StrategyParameterType.Float.value

        self.no_strategy = [
            {'StrategyParameterName': 'PercentageVolume', 'StrategyParameterType': '6',
             'StrategyParameterValue': '0.1'},
            {'StrategyParameterName': 'ChildMinQty', 'StrategyParameterType': '6',
             'StrategyParameterValue': '100'},
        ]
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_partial_fill = Status.PartialFill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_1")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_bid_1)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_bid_2)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, 156, self.price)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_ioc_rule, nos_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid_1)
        market_data_snap_shot.add_fields_into_repeating_group('NoMDEntries', [dict(MDEntryType=0, MDEntryPx=self.price_bid_2, MDEntrySize=self.qty_bid_2, MDEntryPositionNo=2)])
        self.fix_manager_feed_handler.send_message(market_data_snap_shot)
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r_initial, MDEntrySize=self.md_entry_size_incr_r_initial)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(3)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.POV_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_min_value_params()
        self.POV_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.POV_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1)).add_tag(dict(ClientAlgoPolicyID='CustomPOV'))
        self.POV_order.update_repeating_group('NoStrategyParameters', self.no_strategy)

        self.fix_manager_sell.send_message_and_receive_response(self.POV_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(10)

        # region Update LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r, MDEntrySize=self.md_entry_size_incr_r)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        time.sleep(10)
        # endregion

        # region Update LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r, MDEntrySize=self.md_entry_size_incr_r)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(30)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
