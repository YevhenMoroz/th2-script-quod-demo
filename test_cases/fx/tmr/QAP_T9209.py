from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
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


class QAP_T9209(TestCase):
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
        self.fix_manager_pks = FixManager(self.pks_env, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.position_verifier = PositionVerifier(self.test_id)
        self.platinum = self.data_set.get_client_by_name("client_mm_11")
        self.quod2 = self.data_set.get_client_by_name("client_int_2")
        self.mxn_jpy = self.data_set.get_symbol_by_name("symbol_28")
        self.mxn = self.data_set.get_currency_by_name("currency_mxn")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.gbp_usd_spot = {"Symbol": self.mxn_jpy,
                             "SecurityType": self.security_type}
        self.main_rule_result = {"alive": "true", "gatingRuleResultAction": "REJ",
                                 "gatingRuleResultIndice": 1, "gatingRuleResultRejectType": "HRD",
                                 "holdOrder": "false", "splitRatio": 1}
        self.rule = [
            {
                "alive": "true",
                "tradeManagementRuleResult": [
                    {
                        "alive": "true",
                        "hedgeAccountGroupID": self.quod2,
                        "tradeMgtRuleResultRank": 1,
                        "tradeMgtRuleResultAction": "ABO"
                    }
                ],
                "tradeMgtRuleCondExp": "AND(InstrSymbol={},AccountGroupID=Platinum1)".format(self.mxn_jpy),
                "tradeMgtRuleCondName": self.mxn_jpy,
                "tradeMgtRuleCondRank": 1
            },
            {
                "alive": "true",
                "tradeManagementRuleResult": [
                    {
                        "alive": "true",
                        "hedgeAccountGroupID": "amtest",
                        "tradeMgtRuleResultRank": 1,
                        "tradeMgtRuleResultAction": "ABO"
                    }
                ],
                "tradeMgtRuleCondName": "Default Result",
                "tradeMgtRuleCondRank": 2
            }
        ]
        self.instrument = {
            "InstrSymbol": self.mxn_jpy,
            "InstrType": self.data_set.get_fx_instr_type_ja("fx_spot"),
            "SecurityID": self.mxn_jpy,
            "SecurityExchange": "XQFX"
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region find out position of QUOD2
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Account": self.quod2})
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        internal_report_before = self.fix_manager_pks.get_last_message("PositionReport",
                                                                       "'Account': '{}'".format(self.quod2))
        internal_report_before = self.position_verifier.find_position_report_by_type(internal_report_before, "BASE")
        # region Step 1
        self.trade_management_rule.apply_rule(self.rule)
        self.trade_management_rule.enable_trade_management_rule()
        self.rest_manager.send_post_request(self.trade_management_rule)
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.platinum,
                                                                                 "InstrumentBlock": self.instrument,
                                                                                 "Currency": self.mxn})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        self.sleep(2)
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Account": self.quod2})
        self.fix_manager_pks.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        internal_report_after = self.fix_manager_pks.get_last_message("PositionReport",
                                                                      "'Account': '{}'".format(self.quod2))
        internal_report_after = self.position_verifier.find_position_report_by_type(internal_report_after, "BASE")
        # endregion
        # region Step 2
        self.position_verifier.count_position_change(internal_report_before, internal_report_after, 1000000, self.quod2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.trade_management_rule.disable_trade_management_rule()
        self.rest_manager.send_post_request(self.trade_management_rule)
        self.sleep(2)
