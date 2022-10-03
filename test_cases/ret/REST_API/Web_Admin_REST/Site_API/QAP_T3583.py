import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import \
    RestApiInstitutionMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiZoneMessages import RestApiZoneMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiLocationMessages import RestApiLocationMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiDeskMessages import RestApiDeskMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T3583(TestCase):
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
        self.location_message = RestApiLocationMessages(data_set=data_set)
        self.desk_message = RestApiDeskMessages(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        self.institution_id = {'institutionID': 3}
        self.zone_id = {'zoneID': 6}
        self.location_id = {'locationID': 6}
        self.desk_id = {'deskID': 5}
        self.error_message_empty_institution = "invalid request code=QUOD-17:Message format is incorrect," \
                                               " InstitutionID isn't found"
        self.error_message_empty_zone = "invalid request code=QUOD-17:Message format is incorrect, ZoneID isn't found"
        self.error_message_empty_location = "invalid request code=QUOD-17:Message format is incorrect, LocationID isn't found"

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
        test_api_user_pre_condition = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that hierarchical level - 'Institution(id=3)' was set for '{self.test_user}' user.",
                        expected_result=self.institution_id['institutionID'],
                        actual_result=int(test_api_user_pre_condition[0]['institutionID']))
        # endregion

        # region step 3, Check that user with hierarchical level - 'Institution' can not Modify 'Zone' without 'institutionID' field
        self.zone_message.find_all_zone()
        test_zone = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.zone_message),
            filter_dict=self.zone_id)

        test_zone[0].pop('institutionID')
        test_zone[0].pop('alive')
        self.zone_message.modify_zone(custom_params=test_zone[0])
        modify_zone_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.zone_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that user with hierarchical level - Institution can not Modify 'Zone' without"
                                   " 'institutionID' field.",
                        expected_result=self.error_message_empty_institution,
                        actual_result=modify_zone_response)
        # endregion

        # region step 4, Check that user with hierarchical level - 'Institution' can not Create 'Zone' without 'institutionID' field
        self.zone_message.create_zone(custom_params={'zoneName': 'test_api_zone'})
        create_zone_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.zone_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that user with hierarchical level - Institution can not Create 'Zone' without"
                                   " 'institutionID' field.",
                        expected_result=self.error_message_empty_institution,
                        actual_result=create_zone_response)
        # endregion

        # region step 6, Check that user with hierarchical level - 'Institution' can not Modify 'Location' without 'zoneID' field
        self.location_message.find_all_location()
        test_location = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.location_message),
            filter_dict=self.location_id)

        test_location[0].pop('zoneID')
        test_location[0].pop('alive')
        self.location_message.modify_location(custom_params=test_location[0])
        modify_location_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.location_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical level - Institution can not Modify 'Location' without"
                                   " 'zoneID' field.",
                        expected_result=self.error_message_empty_zone,
                        actual_result=modify_location_response)
        # endregion

        # region step 7, Check that user with hierarchical level - 'Institution' can not Create 'Location' without 'zoneID' field
        self.location_message.create_location(custom_params={'locationName': 'test_api_location'})
        create_location_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.location_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical level - Institution can not Create 'Location' without"
                                   "'zoneID' field.",
                        expected_result=self.error_message_empty_zone,
                        actual_result=create_location_response)
        # endregion

        # region step 9, Check that user with hierarchical level - 'Institution' can not Modify 'Desk' without 'locationID' field
        self.desk_message.find_all_desk()
        test_desk = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.desk_message),
            filter_dict=self.desk_id)

        test_desk[0].pop('locationID')
        test_desk[0].pop('alive')
        self.desk_message.modify_desk(custom_params=test_desk[0])
        modify_desk_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.desk_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical level - Institution can not Modify 'Desk' without"
                                   " 'locationID' field.",
                        expected_result=self.error_message_empty_location,
                        actual_result=modify_desk_response)
        print(modify_desk_response)
        # endregion

        # region step 10, Check that user with hierarchical level - 'Institution' can not Create 'Desk' without 'locationID' field
        self.desk_message.create_desk(custom_params={'deskName': 'test_api_desk', 'deskMode': 'CL'})
        create_desk_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.desk_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that user with hierarchical level - Institution can not Create 'Desk' without"
                                   " 'locationID' field.",
                        expected_result=self.error_message_empty_location,
                        actual_result=create_desk_response)
        # endregion

