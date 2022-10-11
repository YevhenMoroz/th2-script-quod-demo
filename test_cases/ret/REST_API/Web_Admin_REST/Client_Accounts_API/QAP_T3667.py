import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Client_Accounts_API.RestApiClientClientGroupMessages import\
    RestApiClientClientGroupMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3667(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_client_client_group_message = RestApiClientClientGroupMessages(data_set=data_set)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.error_message = "invalid request code=QUOD-17:Message format is incorrect, ClientClientGroupID isn't found"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region, step 2, Create new ClientClientGroup without required fields and check result
        self.api_client_client_group_message.create_client_client_group(custom_params={})
        parsed_response = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.api_client_client_group_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that ClientClientGroup was not created without required "
                                   "fields.",
                        expected_result=self.error_message,
                        actual_result=parsed_response)
        # endregion

