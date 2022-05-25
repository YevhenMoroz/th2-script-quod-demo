import os

from custom import basic_custom_actions as bca
from test_cases.wrapper.ret_wrappers import verifier
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Client_Accounts_API.RestApiClientMessages import \
    RestApiClientMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_5360(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_client_message = RestApiClientMessages(data_set=data_set)
        self.api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.tested_client = self.data_set.get_client_by_name("client_5")

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region create new Client and check result - step 2
        self.api_client_message.create_client()
        self.api_manager.send_post_request(api_message=self.api_client_message)

        self.api_client_message.find_all_client()
        client_status_after_creation = self.api_manager.parse_response_details(
            response=self.api_manager.send_get_request(self.api_client_message),
            filter_dict={"accountGroupID": self.tested_client})
        try:
            verifier(case_id=self.test_id,
                     event_name="Check Client Status after creation request",
                     expected_value="true",
                     actual_value=client_status_after_creation[0]["alive"])
        except:
            bca.create_event(f'Fail test event. Response is empty. Step 2',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion

        # region disable Client and check result - step 3
        self.api_client_message.disable_client(client_id=self.tested_client)
        self.api_manager.send_post_request(api_message=self.api_client_message)

        self.api_client_message.find_all_client()
        client_status_after_disable = self.api_manager.parse_response_details(
            response=self.api_manager.send_get_request(self.api_client_message),
            filter_dict={"accountGroupID": self.tested_client})
        try:
            verifier(case_id=self.test_id,
                     event_name="Check Client Status after send disable request",
                     expected_value="false",
                     actual_value=client_status_after_disable[0]["alive"])
        except:
            bca.create_event(f'Fail test event. Response is empty. Step 3',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion

        # region enable Client and check result - step 4
        self.api_client_message.enable_client(client_id=self.tested_client)
        self.api_manager.send_post_request(api_message=self.api_client_message)

        self.api_client_message.find_all_client()
        client_status_after_enable = self.api_manager.parse_response_details(
            response=self.api_manager.send_get_request(self.api_client_message),
            filter_dict={"accountGroupID": self.tested_client})
        try:
            verifier(case_id=self.test_id,
                     event_name="Check Client Status after send enable request",
                     expected_value="true",
                     actual_value=client_status_after_enable[0]["alive"])
        except:
            bca.create_event(f'Fail test event. Response is empty. Step 4',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion
