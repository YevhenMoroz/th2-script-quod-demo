import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiRiskLimitDimensions import \
    RestApiRiskLimitDimensions
from test_framework.core.try_exept_decorator import try_except


class QAP_T3271(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.risk_limit_dimension_message = RestApiRiskLimitDimensions(data_set=data_set)
        self.rules_name = [self.qap_id + f'_api_{count}' for count in range(1, 5)]
        self.user = self.data_set.get_recipient_by_name('recipient_user_2')
        self.security_account = self.data_set.get_account_by_name('account_1')
        self.client = self.data_set.get_client_by_name('client_1')
        self.risk_limit_dimensions = self.data_set.get_risk_limit_dimension_by_name('risk_limit_dimension_1')
        self.error_message_client_account = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                            "allowed combination AccountGroup + SecurityAccount"
        self.error_message_account_client_list = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                                 "allowed combination SecurityAccount + ClientList"
        self.error_message_client_client_list = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                                "allowed combination AccountGroup + ClientList"
        self.error_message_user_desk = "Request fails: code=QUOD-32533:Request not allowed:  Received not allowed " \
                                       "combination User + Desk"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1, create Risk limit Dimension rule without impossible combinations: Account and Client
        parameters_step_1 = {
            "riskLimitDimensionName": self.rules_name[0],
            "riskLimitDimensionDesc": self.rules_name[0],
            "riskLimitDimensionExp": "test",
            "riskLimitDimAccountGroup": [
                {
                    "accountGroupID": self.client
                }
            ],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_1)
        error_response_step_1 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Client + Account",
                        expected_result=self.error_message_client_account,
                        actual_result=error_response_step_1)
        # endregion, step 1

        # region step 2, create Risk limit Dimension rule without impossible combinations: Account and Client List
        parameters_step_2 = {
            "riskLimitDimensionName": self.rules_name[1],
            "riskLimitDimensionDesc": self.rules_name[1],
            "riskLimitDimensionExp": "test",
            "clientListID": self.risk_limit_dimensions["clientListID"],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_2)
        error_response_step_2 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Account + Client List",
                        expected_result=self.error_message_account_client_list,
                        actual_result=error_response_step_2)
        # endregion, step 2

        # region step 3, create Risk limit Dimension rule without impossible combinations: Client and Client List
        parameters_step_3 = {
            "riskLimitDimensionName": self.rules_name[2],
            "riskLimitDimensionDesc": self.rules_name[2],
            "riskLimitDimensionExp": "test",
            "clientListID": self.risk_limit_dimensions["clientListID"],
            "riskLimitDimAccountGroup": [
                {
                    "accountGroupID": self.client
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_3)
        error_response_step_3 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Client + Client List",
                        expected_result=self.error_message_client_client_list,
                        actual_result=error_response_step_3)
        # endregion, step 3

        # region step 4, create Risk limit Dimension rule without impossible combinations: User and Desk
        parameters_step_4 = {
            "riskLimitDimensionName": self.rules_name[3],
            "riskLimitDimensionDesc": self.rules_name[3],
            "riskLimitDimensionExp": "test",
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ],
            "riskLimitDimDesk": [
                {
                    "deskID": self.risk_limit_dimensions["deskID"]
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_4)
        error_response_step_4 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: User + Desk",
                        expected_result=self.error_message_user_desk,
                        actual_result=error_response_step_4)
        # endregion, step 4





