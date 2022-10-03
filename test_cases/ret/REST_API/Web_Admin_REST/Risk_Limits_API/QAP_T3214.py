import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiRiskLimitDimensions import \
    RestApiRiskLimitDimensions
from test_framework.core.try_exept_decorator import try_except


class QAP_T3214(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.risk_limit_dimension_message = RestApiRiskLimitDimensions(data_set=data_set)
        self.rules_name = ['QAP_7534_0',
                           'QAP_7534_1',
                           'QAP_7534_2',
                           'QAP_7534_3',
                           'QAP_7534_4',
                           'QAP_7534_5',
                           'QAP_7534_6',
                           'QAP_7534_7',
                           'QAP_7534_8',
                           'QAP_7534_9',
                           'QAP_7534_10']
        self.user = self.data_set.get_recipient_by_name('recipient_user_2')
        self.security_account = self.data_set.get_account_by_name('account_1')
        self.risk_limit_dimensions = self.data_set.get_risk_limit_dimension_by_name('risk_limit_dimension_1')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1, create risk limit dimension rule with: Account, User, Listing and Instrument Type
        parameters_step_1 = {
            "riskLimitDimensionName": self.rules_name[0],
            "riskLimitDimensionDesc": self.rules_name[0],
            "instrType": self.risk_limit_dimensions["instrType"],
            "listingID": self.risk_limit_dimensions["listingID"],
            "riskLimitDimensionExp": "test",
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_1)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 2, create risk limit dimension rule with: Route, Execution Policy, Trading Phase, Side
        parameters_step_2 = {
            "riskLimitDimensionName": self.rules_name[1],
            "riskLimitDimensionDesc": self.rules_name[1],
            "side": self.risk_limit_dimensions["side"],
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "routeID": self.risk_limit_dimensions["routeID"],
            "riskLimitDimensionExp": "test"
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_2)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 3, create risk limit dimension rule with: Account, Execution Policy, Trading Phase, Side
        parameters_step_3 = {
            "riskLimitDimensionName": self.rules_name[2],
            "riskLimitDimensionDesc": self.rules_name[2],
            "side": self.risk_limit_dimensions["side"],
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ],
            "riskLimitDimensionExp": "test"
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_3)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 4, create risk limit dimension rule with: Route, Execution Policy, Listing, Instrument Type
        parameters_step_4 = {
            "riskLimitDimensionName": self.rules_name[3],
            "riskLimitDimensionDesc": self.rules_name[3],
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "instrType": self.risk_limit_dimensions["instrType"],
            "listingID": self.risk_limit_dimensions["listingID"],
            "routeID": self.risk_limit_dimensions["routeID"],
            "riskLimitDimensionExp": "test"
        }

        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_4)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 5, create risk limit dimension rule: Route, User, Listing, Side
        parameters_step_5 = {
            "riskLimitDimensionName": self.rules_name[4],
            "riskLimitDimensionDesc": self.rules_name[4],
            "listingID": self.risk_limit_dimensions["listingID"],
            "side": self.risk_limit_dimensions["side"],
            "routeID": self.risk_limit_dimensions["routeID"],
            "riskLimitDimensionExp": "test",
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_5)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 6, create risk limit dimension rule: Rote, User, Trading Phase, Instrument Type
        parameters_step_6 = {
            "riskLimitDimensionName": self.rules_name[5],
            "riskLimitDimensionDesc": self.rules_name[5],
            "instrType": self.risk_limit_dimensions["instrType"],
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "routeID": self.risk_limit_dimensions["routeID"],
            "riskLimitDimensionExp": "test",
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_6)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 7, create risk limit dimension rule: Account, User, Trading Phase, Instrument Type
        parameters_step_7 = {
            "riskLimitDimensionName": self.rules_name[6],
            "riskLimitDimensionDesc": self.rules_name[6],
            "riskLimitDimensionExp": "test",
            "instrType": self.risk_limit_dimensions["instrType"],
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_7)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 8, create risk limit dimension rule: Account, User, Listing, Side
        parameters_step_8 = {
            "riskLimitDimensionName": self.rules_name[7],
            "riskLimitDimensionDesc": self.rules_name[7],
            "riskLimitDimensionExp": "test",
            "side": self.risk_limit_dimensions["side"],
            "listingID": self.risk_limit_dimensions["listingID"],
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_8)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 9, create risk limit dimension rule: Account, Execution Policy, Listing, Instrument Type
        parameters_step_9 = {
            "riskLimitDimensionName": self.rules_name[8],
            "riskLimitDimensionDesc": self.rules_name[8],
            "riskLimitDimensionExp": "test",
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "listingID": self.risk_limit_dimensions["listingID"],
            "instrType": self.risk_limit_dimensions["instrType"],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_9)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 10, create risk limit dimension rule: Account, Route, User, Execution Policy
        parameters_step_10 = {
            "riskLimitDimensionName": self.rules_name[9],
            "riskLimitDimensionDesc": self.rules_name[9],
            "riskLimitDimensionExp": "test",
            "executionPolicy": self.risk_limit_dimensions["executionPolicy"],
            "routeID": self.risk_limit_dimensions["routeID"],
            "riskLimitDimUserLogin": [
                {
                    "userID": self.user
                }
            ],
            "riskLimitDimSecurityAccount": [
                {
                    "accountID": self.security_account
                }
            ]
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_10)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region step 11, create risk limit dimension rule: Listing, Trading Phase, Instrument Type, Side
        parameters_step_11 = {
            "riskLimitDimensionName": self.rules_name[10],
            "riskLimitDimensionDesc": self.rules_name[10],
            "riskLimitDimensionExp": "test",
            "side": self.risk_limit_dimensions["side"],
            "listingID": self.risk_limit_dimensions["listingID"],
            "standardTradingPhase": self.risk_limit_dimensions["standardTradingPhase"],
            "instrType": self.risk_limit_dimensions["instrType"],
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_11)
        self.wa_api_manager.send_post_request(self.risk_limit_dimension_message)
        # endregion

        # region verification, check that all rules are created with all entered fields
        self.risk_limit_dimension_message.find_all_risk_limit_dimension()
        parsed_response = self.wa_api_manager.send_get_request(self.risk_limit_dimension_message)

        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[0], parameters_step_1, 1)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[1], parameters_step_2, 2)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[2], parameters_step_3, 3)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[3], parameters_step_4, 4)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[4], parameters_step_5, 5)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[5], parameters_step_6, 6)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[6], parameters_step_7, 7)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[7], parameters_step_8, 8)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[8], parameters_step_9, 9)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[9], parameters_step_10, 10)
        self.wa_api_manager.risk_limit_dimension_verifier(self.test_id, parsed_response, self.rules_name[10], parameters_step_11, 11)
        # endregion







