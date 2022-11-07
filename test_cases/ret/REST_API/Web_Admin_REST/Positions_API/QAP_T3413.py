import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import RestApiInstitutionMessages
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiWashBookMessages import RestApiWashBookMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T3413(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.id, report_id)
        self.session_alias_wa_site = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.session_alias_wa_test = self.environment.get_list_web_admin_rest_api_environment()[1].session_alias_wa
        self.wa_api_manager_site = WebAdminRestApiManager(session_alias=self.session_alias_wa_site,
                                                          case_id=self.test_id)
        self.wa_api_manager_test = WebAdminRestApiManager(session_alias=self.session_alias_wa_test,
                                                          case_id=self.test_id)
        self.user_message = RestApiUserMessages(data_set=data_set)
        self.institution_message = RestApiInstitutionMessages(data_set=data_set)
        self.wash_book_messages = RestApiWashBookMessages(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        self.hierarchical_level_test = self.data_set.get_hierarchical_level_by_name('hierarchical_level_2')
        self.institution_id = self.hierarchical_level_test['institutionID']
        self.wash_book_name = f"api_wash_book_{self.id}"

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

        # region step 4, Create new Wash Book with tested institution id and check result
        self.wash_book_messages.create_security_account(wash_book_name=self.wash_book_name,
                                                        institution_id=self.institution_id['institutionID'])
        new_wash_book = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_multiple_request(self.wash_book_messages),
            filter_dict={'accountID': self.wash_book_name}
        )
        data_validation(test_id=self.test_id,
                        event_name=f"Check that new Wash Book '{self.wash_book_name}' was created.",
                        expected_result=self.wash_book_name,
                        actual_result=new_wash_book[0]['accountID'])
        # endregion

        # step 5, Enable existing wash book
        self.wash_book_messages.disable_security_account(account_id=self.wash_book_name)
        self.wa_api_manager_test.send_post_request(self.wash_book_messages)

        self.wash_book_messages.find_all_security_account_wash_book()
        disabled_wash_book = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.wash_book_messages),
            filter_dict={'accountID': self.wash_book_name}
        )
        data_validation(test_id=self.test_id,
                        event_name=f"Check that Wash Book '{self.wash_book_name}' was disabled.",
                        expected_result="false",
                        actual_result=disabled_wash_book[0]['alive'])
        # endregion

        # step 6, Disable existing wash book
        self.wash_book_messages.enable_security_account(account_id=self.wash_book_name)
        self.wa_api_manager_test.send_post_request(self.wash_book_messages)

        self.wash_book_messages.find_all_security_account_wash_book()
        disabled_wash_book = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.wash_book_messages),
            filter_dict={'accountID': self.wash_book_name}
        )
        data_validation(test_id=self.test_id,
                        event_name=f"Check that Wash Book '{self.wash_book_name}' was enabled.",
                        expected_result="true",
                        actual_result=disabled_wash_book[0]['alive'])
        # endregion

