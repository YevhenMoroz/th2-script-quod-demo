import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiRiskLimitDimensions import \
    RestApiRiskLimitDimensions
from test_framework.core.try_exept_decorator import try_except


class RiskLimitDimensionDeleter(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.risk_limit_dimension_message = RestApiRiskLimitDimensions(data_set=data_set)
        self.rules_name = [self.qap_id + f'_api_{count}' for count in range(1, 6)]
        self.risk_limit_dimensions = self.data_set.get_risk_limit_dimension_by_name('risk_limit_dimension_1')
        self.pattern = 'QAP'

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        self.risk_limit_dimension_message.find_all_risk_limit_dimension()
        response = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.risk_limit_dimension_message))
        print(f"Rules count: {len(response)}")
        for count in range(len(response)):
            for key, value in response[count].items():
                if key == 'riskLimitDimensionName':
                    if self.pattern in value:
                        rule_id = response[count]['riskLimitDimensionID']
                        self.risk_limit_dimension_message.delete_risk_limit_dimension(risk_limit_dimension_id=rule_id)
                        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)




