import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_6302(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_washbook_rule_message = RestApiWashBookRuleMessages(data_set=data_set)
        self.api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.tested_washbook_rule_name = "api_washbook_rule_6302"

    @staticmethod
    def check_washbook_rule_status(response, tested_washbook_rule_name, test_id):

        washbook_rule_status = True
        for count in range(len(response)):
            rule_name = response[count]["washBookRuleName"]
            if rule_name == tested_washbook_rule_name:
                bca.create_event(f'Fail test event, {tested_washbook_rule_name} is present on the Web Admin',
                                 status='FAILED',
                                 parent_id=test_id)
                washbook_rule_status = False
                break
        if washbook_rule_status:
            bca.create_event(f'Passed test event, {tested_washbook_rule_name} is not present on the Web Admin',
                             status='SUCCESS',
                             parent_id=test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region Create new WashBookRule without required field - institutionID and Verify response - step 1
        self.api_washbook_rule_message.create_washbook_rule()
        self.api_washbook_rule_message.remove_parameter(parameter_name='institutionID')
        self.api_washbook_rule_message.update_parameters({'washBookRuleName': self.tested_washbook_rule_name})
        self.api_manager.send_post_request(self.api_washbook_rule_message)

        self.api_washbook_rule_message.find_all_washbook_rule()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_rule_message))
            self.check_washbook_rule_status(parsed_response, self.tested_washbook_rule_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Create new WashBookRule without required field - washBookAccountID and Verify response - step 2
        self.api_washbook_rule_message.create_washbook_rule()
        self.api_washbook_rule_message.remove_parameter(parameter_name='washBookAccountID')
        self.api_washbook_rule_message.update_parameters({'washBookRuleName': self.tested_washbook_rule_name})
        self.api_manager.send_post_request(self.api_washbook_rule_message)

        self.api_washbook_rule_message.find_all_washbook_rule()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_rule_message))
            self.check_washbook_rule_status(parsed_response, self.tested_washbook_rule_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Create new WashBookRule without required field - washBookRuleName and Verify response - step 3
        self.api_washbook_rule_message.create_washbook_rule()
        self.api_washbook_rule_message.remove_parameter(parameter_name='washBookRuleName')
        self.api_manager.send_post_request(self.api_washbook_rule_message)

        self.api_washbook_rule_message.find_all_washbook_rule()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_rule_message))
            self.check_washbook_rule_status(parsed_response, self.api_washbook_rule_message.default_washbook_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
