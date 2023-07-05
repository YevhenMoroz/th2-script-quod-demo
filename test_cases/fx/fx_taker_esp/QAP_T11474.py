from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportTakerMO import FixMessageExecutionReportTakerMO
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiGatingRuleMessages import RestApiGatingRuleMessages


class QAP_T11474(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.buy_side_esp_env = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.rest_api_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.gating_rule = RestApiGatingRuleMessages()
        self.rest_manager = RestApiManager(self.rest_api_env, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportTakerMO()
        self.fix_manager = FixManager(self.buy_side_esp_env, self.test_id)
        self.fix_verifier = FixVerifier(self.buy_side_esp_env, self.test_id)
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.gbp_usd_spot = {"Symbol": self.gbp_usd,
                             "SecurityType": self.security_type}
        self.main_rule_result = {"alive": "true", "gatingRuleResultAction": "REJ",
                                       "gatingRuleResultIndice": 1, "gatingRuleResultRejectType": "HRD",
                                       "holdOrder": "false", "splitRatio": 1}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.gating_rule.set_main_rule_evaluation()
        self.gating_rule.change_result_by_index(self.main_rule_result)
        self.gating_rule.modify_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.gating_rule.enable_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.gating_rule.set_evaluation_rule()
        self.gating_rule.change_result_by_index(self.main_rule_result)
        self.gating_rule.modify_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.gating_rule.enable_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.sleep(1)
        # region Step 1
        self.new_order.set_default_mo().change_parameters(
            {"Currency": self.gbp, "Instrument": self.gbp_usd_spot})
        self.fix_manager.send_message_and_receive_response(self.new_order)
        # endregion
        # Region Step 2
        self.execution_report.set_params_from_new_order_single(self.new_order, status=Status.Reject)
        self.execution_report.add_tag(
            {"GatingRuleCondName": "First Main", "GatingRuleName": "Main Rule", "LastMkt": "*"})
        self.execution_report.remove_parameter("OrdRejReason")
        self.execution_report.add_tag({"OrderCapacity": "*"})
        self.execution_report.change_parameter("Text", "order rejected as per gating rule instruction")
        # endregion
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["trailer", "header"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.gating_rule.set_main_rule_evaluation()
        self.gating_rule.disable_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.gating_rule.set_evaluation_rule()
        self.gating_rule.disable_gating_rule()
        self.rest_manager.send_post_request(self.gating_rule)
        self.sleep(2)
