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


class QAP_T3605(TestCase):
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
        self.hierarchical_level_test = self.data_set.get_hierarchical_level_by_name('hierarchical_level_2')
        self.zone_id = self.hierarchical_level_test['zoneID']
        self.location_id = self.hierarchical_level_test['locationID']
        self.desk_id = self.hierarchical_level_test['deskID']
        self.user_desk = 'user_desk'

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
        test_api_user_pre_condition = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that hierarchical level - 'Zone(id=6)' was set for '{self.test_user}' user.",
                        expected_result=self.zone_id['zoneID'],
                        actual_result=int(test_api_user_pre_condition[0]['zoneID']))
        # endregion

        # region step 2, Check that user with hierarchical leve - Zone can set Location level for the user from same hierarchy
        self.user_message.find_user(user_id=self.user_desk)
        user_desk = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.user_message))
        new_user_location_parameters = hierarchical_level_updater(test_id=self.test_id, user_response=user_desk,
                                                                  new_hierarchical_assignment=self.location_id)
        self.user_message.modify_user(custom_params=new_user_location_parameters)
        self.wa_api_manager_test.send_post_request(self.user_message)

        self.user_message.find_user(user_id=self.user_desk)
        user_location = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical leve - Zone"
                                   " can set Location level for the user from same hierarchy.",
                        expected_result=self.location_id['locationID'],
                        actual_result=int(user_location[0]['location']))
        # endregion

        # region step 3, Check that user with hierarchical leve - Zone can set Desk level for the user from same hierarchy
        new_user_desk_parameters = hierarchical_level_updater(test_id=self.test_id, user_response=user_desk,
                                                                  new_hierarchical_assignment=self.desk_id)
        self.user_message.modify_user(custom_params=new_user_desk_parameters)
        self.wa_api_manager_test.send_post_request(self.user_message)

        self.user_message.find_user(user_id=self.user_desk)
        user_desk = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical leve - Zone"
                                   " can set Desk level for the user from same hierarchy.",
                        expected_result=self.desk_id['deskID']['deskUserRole'][0]['deskID'],
                        actual_result=int(user_desk[0]['deskUserRole'][0]['deskID']))
        # endregion

