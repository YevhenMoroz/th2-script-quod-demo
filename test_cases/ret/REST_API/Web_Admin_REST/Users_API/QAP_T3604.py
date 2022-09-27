import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiZoneMessages import RestApiZoneMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T3604(TestCase):
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
        self.zone_message = RestApiZoneMessages(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        self.zone_id = {'zoneID': 6}
        self.location_id = {'locationID': 6}
        self.desk_id = {'deskUserRole': [{'deskID': 5}]}
        self.error_message_step2 = "Request fails: code=QUOD-32533:Request not allowed:  HierarchicalLevel validations:" \
                             " User adm_rest is not allowed to execute Adminmonitoring_UserModificationRequest"
        self.error_message_step3 = "Request fails: code=QUOD-32264:The user can't belongs" \
                                   " to a location and a desk at the same time"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-Condition, set hierarchical level - Zone for test user and check result
        self.user_message.find_user(user_id=self.test_user)
        test_api_user = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))

        new_user_parameters = hierarchical_level_updater(test_id=self.test_id, user_response=test_api_user,
                                                         new_hierarchical_assignment=self.zone_id)
        self.user_message.modify_user(custom_params=new_user_parameters)
        self.wa_api_manager_site.send_post_request(self.user_message)

        self.user_message.find_user(user_id=self.test_user)
        test_api_user = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that hierarchical level - 'Zone(id=6)' was set for '{self.test_user}' user.",
                        expected_result=self.zone_id['zoneID'],
                        actual_result=int(test_api_user[0]['zoneID']))
        # endregion

        # region step 2, Check that user with hierarchical level - Zone can not modify a user without hierarchical assignments
        test_api_user[0].pop('zoneID')
        self.user_message.modify_user(custom_params=test_api_user[0])
        user_response_step2 = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that user with hierarchical level - Zone"
                                   f" can not modify a user without hierarchical assignments",
                        expected_result=self.error_message_step2,
                        actual_result=user_response_step2)
        # endregion

        # region step 3, Check that user with hierarchical level - Zone can not set 2 hierarchical assignment at time
        test_api_user[0].update(self.location_id)
        test_api_user[0].update(self.desk_id)
        self.user_message.modify_user(custom_params=test_api_user[0])
        user_response_step3 = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical level - Zone"
                                   " can not set 2 hierarchical assignment at time",
                        expected_result=self.error_message_step3,
                        actual_result=user_response_step3)
        # endregion



