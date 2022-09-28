import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Client_Accounts_API.RestApiClientMessages import \
    RestApiClientMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3804(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_client_message = RestApiClientMessages(data_set=data_set)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.client = self.data_set.get_client_by_name("client_5")
        self.error_message = "invalid request code=QUOD-17:Message format is incorrect, DiscloseExec isn\'t found"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region, Modify existing client removing required field - "Disclose Exec"
        self.api_client_message.find_all_client()
        tested_client = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.api_client_message),
            filter_dict={'clientAccountGroupID': self.client})
        data_validation(test_id=self.test_id,
                        event_name=f"Check that '{self.client}' is present",
                        expected_result="true",
                        actual_result=tested_client[0]["alive"])
        self.api_client_message.modify_client(tested_client[0])
        self.api_client_message.remove_parameter(parameter_name="discloseExec")
        error_response = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.api_client_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that '{self.client}' was not modified without required "
                                   "field - 'Disclose Exec'",
                        expected_result=self.error_message,
                        actual_result=error_response)
        # endregion
