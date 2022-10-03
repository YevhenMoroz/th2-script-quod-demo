import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import RestApiInstitutionMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiZoneMessages import RestApiZoneMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T3581(TestCase):
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
        self.institution_message = RestApiInstitutionMessages(data_set=data_set)
        self.zone_message = RestApiZoneMessages(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        self.zone_id = {'zoneID': 6}
        self.error_message_zone = "Request fails: code=QUOD-32533:Request not allowed:" \
                                  "  User with HierarchicalLevel=Zone can not impact Zone entity"
        self.error_message_institution = "Request fails: code=QUOD-32533:Request not allowed:" \
                                         "  User with HierarchicalLevel=Zone can not impact Institution entity"

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

        # region step 1, Check that user with hierarchical level - Zone does not have access to a 'Zone' entity's
        self.zone_message.create_zone(custom_params={'institutionID': 3, 'zoneName': 'test_api_zone'})
        zone_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.zone_message))
        data_validation(test_id=self.test_id,
                        event_name='Check that user with hierarchical level - Zone can not create a new Zone',
                        expected_result=self.error_message_zone,
                        actual_result=zone_response)
        # endregion

        # region step 2, Check that user with hierarchical level - Zone does not have access to a 'Institution' entity's
        self.institution_message.create_institution()
        institution_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.institution_message))
        data_validation(test_id=self.test_id,
                        event_name='Check that user with hierarchical level - Zone can not create a new Institution',
                        expected_result=self.error_message_institution,
                        actual_result=institution_response)
        # endregion
