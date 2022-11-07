import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiWashBookMessages import RestApiWashBookMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3481(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_washbook_message = RestApiWashBookMessages(data_set=data_set)
        self.api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.tested_washbook_name = "api_wash_book_6304_1"
        self.washbook_parameters = {
            "accountID": self.tested_washbook_name,
            "accountDesc": self.tested_washbook_name,
            "clientAccountID": self.tested_washbook_name,
            "clientAccountIDSource": "BIC",
            "isWashBook": "true",
            "institutionID": 1,
            "alive": "true"
        }

    @staticmethod
    def check_washbook_status(response, tested_washbook_name, test_id):

        washbook_status = True
        for count in range(len(response)):
            account = response[count]['accountID']
            if account == tested_washbook_name:
                bca.create_event(f'Fail test event, {tested_washbook_name} is present on the Web Admin',
                                 status='FAILED',
                                 parent_id=test_id)
                washbook_status = False
                break
        if washbook_status:
            bca.create_event(f'Passed test event, {tested_washbook_name} is not present on the Web Admin',
                             status='SUCCESS',
                             parent_id=test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create new WashBookRule without required field - accountID and Verify response - step 1
        self.washbook_parameters.pop('accountID')
        self.api_washbook_message.create_security_account(custom_params=self.washbook_parameters)
        self.api_manager.send_post_request(self.api_washbook_message)

        self.api_washbook_message.find_all_security_account_wash_book()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_message))
            self.check_washbook_status(parsed_response, self.tested_washbook_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Create new WashBookRule without required field - clientAccountIDSource and Verify response - step 2
        self.washbook_parameters.pop('clientAccountIDSource')
        self.washbook_parameters.update({'accountID': self.tested_washbook_name})
        self.api_washbook_message.create_security_account(custom_params=self.washbook_parameters)
        self.api_manager.send_post_request(self.api_washbook_message)

        self.api_washbook_message.find_all_security_account_wash_book()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_message))
            self.check_washbook_status(parsed_response, self.tested_washbook_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Create new WashBookRule without required field - clientAccountID and Verify response - step 3
        self.washbook_parameters.pop('clientAccountID')
        self.washbook_parameters.update({'clientAccountIDSource': 'BIC'})
        self.api_washbook_message.create_security_account(custom_params=self.washbook_parameters)
        self.api_manager.send_post_request(self.api_washbook_message)

        self.api_washbook_message.find_all_security_account_wash_book()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_message))
            self.check_washbook_status(parsed_response, self.tested_washbook_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Create new WashBookRule without required field - institutionID and Verify response - step 4
        self.washbook_parameters.pop('institutionID')
        self.washbook_parameters.update({'clientAccountID': self.tested_washbook_name})
        self.api_washbook_message.create_security_account(custom_params=self.washbook_parameters)
        self.api_manager.send_post_request(self.api_washbook_message)

        self.api_washbook_message.find_all_security_account_wash_book()
        try:
            parsed_response = self.api_manager.parse_response_details(
                response=self.api_manager.send_get_request(self.api_washbook_message))
            self.check_washbook_status(parsed_response, self.tested_washbook_name, self.test_id)
        except:
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
