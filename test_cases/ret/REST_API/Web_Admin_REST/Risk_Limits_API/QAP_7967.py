import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiRiskLimitDimensions import \
    RestApiRiskLimitDimensions
from test_framework.core.try_exept_decorator import try_except


class QAP_7967(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.risk_limit_dimension_message = RestApiRiskLimitDimensions(data_set=data_set)
        self.rules_name = [self.qap_id + f'_api_{count}' for count in range(1, 6)]
        self.risk_limit_dimensions = self.data_set.get_risk_limit_dimension_by_name('risk_limit_dimension_1')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1, create risk limit dimension rule with: Instrument type, Position Type, Settlement Type and
        # Position Validity
        parameters_step_1 = {
            "riskLimitDimensionName": self.rules_name[0],
            "riskLimitDimensionDesc": self.rules_name[0],
            "riskLimitDimensionExp": "test",
            "instrType": self.risk_limit_dimensions["instrType"],
            "positionType": self.risk_limit_dimensions["positionType"][0],
            "settlType": self.risk_limit_dimensions["settlType"][0],
            "posValidity": self.risk_limit_dimensions["posValidity"][0]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_1)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 2, create risk limit dimension rule with: Route, Position Type, Settlement Type and
        # Position Validity
        parameters_step_2 = {
            "riskLimitDimensionName": self.rules_name[1],
            "riskLimitDimensionDesc": self.rules_name[1],
            "riskLimitDimensionExp": "test",
            "routeID": self.risk_limit_dimensions["routeID"],
            "positionType": self.risk_limit_dimensions["positionType"][1],
            "settlType": self.risk_limit_dimensions["settlType"][1],
            "posValidity": self.risk_limit_dimensions["posValidity"][1]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_2)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 3, create risk limit dimension rule with: Execution Policy, Position Type, Settlement Type and
        # Position Validity
        parameters_step_3 = {
            "riskLimitDimensionName": self.rules_name[2],
            "riskLimitDimensionDesc": self.rules_name[2],
            "riskLimitDimensionExp": "test",
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "positionType": self.risk_limit_dimensions["positionType"][2],
            "settlType": self.risk_limit_dimensions["settlType"][2],
            "posValidity": self.risk_limit_dimensions["posValidity"][2]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_3)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 4, create risk limit dimension rule with: Trading Phase, Position Type, Settlement Type and
        # Position Validity
        parameters_step_4 = {
            "riskLimitDimensionName": self.rules_name[3],
            "riskLimitDimensionDesc": self.rules_name[3],
            "riskLimitDimensionExp": "test",
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "positionType": self.risk_limit_dimensions["positionType"][0],
            "settlType": self.risk_limit_dimensions["settlType"][3],
            "posValidity": self.risk_limit_dimensions["posValidity"][3]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_4)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 5, create risk limit dimension rule with: Side, Position Type, Settlement Type and
        # Position Validity
        parameters_step_5 = {
            "riskLimitDimensionName": self.rules_name[4],
            "riskLimitDimensionDesc": self.rules_name[4],
            "riskLimitDimensionExp": "test",
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "positionType": self.risk_limit_dimensions["positionType"][1],
            "settlType": self.risk_limit_dimensions["settlType"][4],
            "posValidity": self.risk_limit_dimensions["posValidity"][4]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_5)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region verification, check that all rules are created with all entered fields
        self.risk_limit_dimension_message.find_all_risk_limit_dimension()
        parsed_response = self.wa_api_manager.send_get_request(self.risk_limit_dimension_message)

        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[0],
                                                          parameters_step_1, 1)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[1],
                                                          parameters_step_2, 2)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[2],
                                                          parameters_step_3, 3)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[3],
                                                          parameters_step_4, 4)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[4],
                                                          parameters_step_5, 5)
        # endregion







