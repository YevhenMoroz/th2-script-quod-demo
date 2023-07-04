from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import PosAmtType
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportTakerMO import FixMessageExecutionReportTakerMO
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiTradeManagementRuleMessages import RestApiTradeManagementRuleMessages


class QAP_T10794(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_env = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.trade_management_rule = RestApiTradeManagementRuleMessages()
        self.trade_request = TradeEntryRequestFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.rest_manager = RestApiManager(self.rest_api_env, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportTakerMO()
        self.position_report_int = FixMessageRequestForPositionsAckFX()
        self.fix_manager_pks = FixManager(self.pks_env, self.test_id)
        self.fix_verifier_pks = FixVerifier(self.pks_env, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.position_verifier = PositionVerifier(self.test_id)
        self.platinum = self.data_set.get_client_by_name("client_mm_11")
        self.quod2 = self.data_set.get_client_by_name("client_int_2")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.base = PosAmtType.BasePosition
        self.gbp_usd_spot = {"Symbol": self.gbp_usd,
                             "SecurityType": self.security_type}
        self.main_rule_result = {"alive": "true", "gatingRuleResultAction": "REJ",
                                 "gatingRuleResultIndice": 1, "gatingRuleResultRejectType": "HRD",
                                 "holdOrder": "false", "splitRatio": 1}
        self.rule = {
            "tradeMgtRuleName": "QAP-T10794_automation", "tradeMgtRuleID": 3400054, "enableSchedule": "false",
            "alive": "false",
            "tradeManagementRuleCondition": [{"alive": "false", "tradeManagementRuleResult": [
                {"alive": "false", "hedgeAccountGroupID": "QUOD2", "tradeMgtRuleResultRank": 1,
                 "tradeMgtRuleResultAction": "ABO"}],
                                              "tradeMgtRuleCondExp": f"AND(OrdrMisc0=OrdrMisc0,OrdrMisc1=OrdrMisc1,"
                                                                     f"OrdrMisc2=OrdrMisc2, OrdrMisc3=OrdrMisc3,"
                                                                     f"OrdrMisc4=OrdrMisc4,OrdrMisc5=OrdrMisc5,"
                                                                     f"OrdrMisc6=OrdrMisc6,OrdrMisc7=OrdrMisc7,"
                                                                     f"OrdrMisc8=OrdrMisc8, OrdrMisc9=OrdrMisc9,"
                                                                     f"ExecMisc0=ExecMisc0,ExecMisc1=ExecMisc1,"
                                                                     f"ExecMisc2=ExecMisc2,ExecMisc3=ExecMisc3,"
                                                                     f"ExecMisc4=ExecMisc4, ExecMisc5=ExecMisc5,"
                                                                     f"ExecMisc6=ExecMisc6,ExecMisc7=ExecMisc7,"
                                                                     f"ExecMisc8=ExecMisc8,ExecMisc9=ExecMisc9,"
                                                                     f"AccountGroupID=Platinum1)",
                                              "tradeMgtRuleCondName": "ordr_exec_miscs", "tradeMgtRuleCondRank": 1},
                                             {"alive": "false",
                                              "tradeManagementRuleResult": [
                                                  {"alive": "false", "hedgeAccountGroupID": "amtest",
                                                   "tradeMgtRuleResultRank": 1,
                                                   "tradeMgtRuleResultAction": "ABO"}
                                              ],
                                              "tradeMgtRuleCondName": "Default Result", "tradeMgtRuleCondRank": 2}]}
        self.exec_misc = {
            "ExecMisc0": "ExecMisc0", "ExecMisc1": "ExecMisc1", "ExecMisc2": "ExecMisc2", "ExecMisc3": "ExecMisc3",
            "ExecMisc4": "ExecMisc4", "ExecMisc5": "ExecMisc5", "ExecMisc6": "ExecMisc6", "ExecMisc7": "ExecMisc7",
            "ExecMisc8": "ExecMisc8", "ExecMisc9": "ExecMisc9",
        }
        self.ordr_misc = {
            "OrdrMisc0": "OrdrMisc0", "OrdrMisc1": "OrdrMisc1", "OrdrMisc2": "OrdrMisc2", "OrdrMisc3": "OrdrMisc3",
            "OrdrMisc4": "OrdrMisc4", "OrdrMisc5": "OrdrMisc5", "OrdrMisc6": "OrdrMisc6", "OrdrMisc7": "OrdrMisc7",
            "OrdrMisc8": "OrdrMisc8", "OrdrMisc9": "OrdrMisc9",
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region find out position of QUOD2
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Account": self.quod2})
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        internal_report_before = self.fix_manager_pks.get_last_message("PositionReport",
                                                                       "'Account': '{}'".format(self.quod2))
        internal_report_before = self.position_verifier.get_amount(internal_report_before, self.base)
        # region Step 1
        self.trade_management_rule.apply_rule(self.rule)
        self.trade_management_rule.enable_trade_management_rule()
        self.rest_manager.send_post_request(self.trade_management_rule)
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.platinum,
                                                                                 "ExecMiscBlock": self.exec_misc,
                                                                                 "OrdrMiscBlock": self.ordr_misc})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.sleep(2)
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Account": self.quod2})
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        internal_report_after = self.fix_manager_pks.get_last_message("PositionReport",
                                                                      "'Account': '{}'".format(self.quod2))
        internal_report_after = self.position_verifier.get_amount(internal_report_after, self.base)
        # endregion
        # region Step 2
        self.position_verifier.count_position_change(internal_report_before, internal_report_after, -1000000, self.quod2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.trade_management_rule.disable_trade_management_rule()
        self.rest_manager.send_post_request(self.trade_management_rule)
        self.sleep(2)
