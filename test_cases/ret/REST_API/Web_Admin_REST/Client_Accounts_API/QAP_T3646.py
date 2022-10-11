import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import \
    RestApiInstitutionMessages
from test_framework.rest_api_wrappers.web_admin_api.Client_Accounts_API.RestApiClientMessages import RestApiClientMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T3646(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa_site = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.session_alias_wa_test = self.environment.get_list_web_admin_rest_api_environment()[1].session_alias_wa
        self.wa_api_manager_site = WebAdminRestApiManager(session_alias=self.session_alias_wa_site,
                                                          case_id=self.test_id)
        self.wa_api_manager_test = WebAdminRestApiManager(session_alias=self.session_alias_wa_test,
                                                          case_id=self.test_id)
        self.user_message = RestApiUserMessages(data_set=data_set)
        self.client_messages = RestApiClientMessages(data_set=data_set)
        self.institution_message = RestApiInstitutionMessages(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        self.hierarchical_level_test = self.data_set.get_hierarchical_level_by_name('hierarchical_level_2')
        self.test_client = self.data_set.get_client_by_name('client_5')
        self.institution_id = self.hierarchical_level_test['institutionID']
        self.desk_id = self.hierarchical_level_test['deskID']['deskUserRole']
        self.new_client = "client_" + os.path.basename(__file__)[:-3]

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-Condition, set hierarchical level - Institution for test user and check result
        self.user_message.find_user(user_id=self.test_user)
        test_api_user = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))

        new_user_parameters = hierarchical_level_updater(test_id=self.test_id, user_response=test_api_user,
                                                         new_hierarchical_assignment=self.institution_id)
        self.user_message.modify_user(custom_params=new_user_parameters)
        self.wa_api_manager_site.send_post_request(self.user_message)

        self.user_message.find_user(user_id=self.test_user)
        test_api_user = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that hierarchical level - 'Institution(id=3)' was set for '{self.test_user}' user.",
                        expected_result=self.institution_id['institutionID'],
                        actual_result=int(test_api_user[0]['institutionID']))
        # endregion

        # region step 2, disable test client and check result
        self.client_messages.disable_client(client_id=self.test_client)
        self.wa_api_manager_test.send_post_request(self.client_messages)

        self.client_messages.find_all_client()
        disabled_client = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.client_messages),
            filter_dict={'accountGroupName': self.test_client}
        )
        data_validation(test_id=self.test_id,
                        event_name=f"Check that '{self.test_client}' is disabled",
                        expected_result='false',
                        actual_result=disabled_client[0]['alive'])
        # endregion

        # region step 3, enable test client
        self.client_messages.enable_client(client_id=self.test_client)
        self.wa_api_manager_test.send_post_request(self.client_messages)

        self.client_messages.find_all_client()
        enabled_client = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.client_messages),
            filter_dict={'accountGroupName': self.test_client}
        )
        data_validation(test_id=self.test_id,
                        event_name=f"Check that '{self.test_client}' is enabled",
                        expected_result='true',
                        actual_result=enabled_client[0]['alive'])
        # endregion

        # region step 4, create a new client
        self.client_messages.create_client(client_name=self.new_client, desk_id=self.desk_id)
        self.wa_api_manager_test.send_post_request(self.client_messages)

        self.client_messages.find_all_client()
        new_client = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.client_messages),
            filter_dict={'accountGroupName': self.new_client}
        )
        if 'accountGroupName' in new_client[0].keys():
            bca.create_event(f"Check that client '{self.new_client}' is created", parent_id=self.test_id)
        # endregion
