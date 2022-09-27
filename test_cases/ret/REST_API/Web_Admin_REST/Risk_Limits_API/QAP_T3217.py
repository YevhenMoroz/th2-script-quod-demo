import os

from test_framework.rest_api_wrappers.utils.verifier import data_validation
from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiRiskLimitDimensions import \
    RestApiRiskLimitDimensions
from test_framework.core.try_exept_decorator import try_except


class QAP_T3217(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.risk_limit_dimension_message = RestApiRiskLimitDimensions(data_set=data_set)
        self.rules_name = [self.qap_id + f'_api_{count}' for count in range(1, 7)]
        self.user = self.data_set.get_recipient_by_name('recipient_user_2')
        self.security_account = self.data_set.get_account_by_name('account_1')
        self.client = self.data_set.get_client_by_name('client_1')
        self.risk_limit_dimensions = self.data_set.get_risk_limit_dimension_by_name('risk_limit_dimension_1')
        self.error_message_listing_listing_group = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                                   "allowed combination Listing + ListingGroup"
        self.error_message_venue_sub_venue = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                             "allowed combination Venue + SubVenue"
        self.error_message_listing_venue = "Request fails: code=QUOD-32533:Request not allowed:  Received not allowed " \
                                           "combination Listing + Venue"
        self.error_message_listing_sub_venue = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                               "allowed combination Listing + SubVenue"
        self.error_message_listing_group_venue = "Request fails: code=QUOD-32533:Request not allowed:  Received not " \
                                                 "allowed combination ListingGroup + Venue"
        self.error_message_listing_group_sub_venue = "Request fails: code=QUOD-32533:Request not allowed:  Received " \
                                                     "not allowed combination ListingGroup + SubVenue"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1, create Risk limit Dimension rule without impossible combination Listing + ListingGroup
        parameters_step_1 = {
            "riskLimitDimensionName": self.rules_name[0],
            "riskLimitDimensionDesc": self.rules_name[0],
            "riskLimitDimensionExp": "test",
            "listingID": self.risk_limit_dimensions['listingID'],
            "listingGroupID": self.risk_limit_dimensions['listingGroupID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_1)
        error_response_step_1 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Listing + ListingGroup",
                        expected_result=self.error_message_listing_listing_group,
                        actual_result=error_response_step_1)
        # endregion, step 1

        # region step 2, create Risk limit Dimension rule without impossible combination Venue + SubVenue
        parameters_step_2 = {
            "riskLimitDimensionName": self.rules_name[1],
            "riskLimitDimensionDesc": self.rules_name[1],
            "riskLimitDimensionExp": "test",
            "venueID": self.risk_limit_dimensions['venueID'],
            "subVenueID": self.risk_limit_dimensions['subVenueID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_2)
        error_response_step_2 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Venue + SubVenue",
                        expected_result=self.error_message_venue_sub_venue,
                        actual_result=error_response_step_2)
        # endregion, step 2

        # region step 3, create Risk limit Dimension rule without impossible combination Listing + Venue
        parameters_step_3 = {
            "riskLimitDimensionName": self.rules_name[2],
            "riskLimitDimensionDesc": self.rules_name[2],
            "riskLimitDimensionExp": "test",
            "venueID": self.risk_limit_dimensions['venueID'],
            "listingID": self.risk_limit_dimensions['listingID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_3)
        error_response_step_3 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Listing + Venue",
                        expected_result=self.error_message_listing_venue,
                        actual_result=error_response_step_3)
        # endregion, step 3

        # region step 4, create Risk limit Dimension rule without impossible combination Listing + SubVenue
        parameters_step_4 = {
            "riskLimitDimensionName": self.rules_name[3],
            "riskLimitDimensionDesc": self.rules_name[3],
            "riskLimitDimensionExp": "test",
            "subVenueID": self.risk_limit_dimensions['subVenueID'],
            "listingID": self.risk_limit_dimensions['listingID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_4)
        error_response_step_4 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: Listing + SubVenue",
                        expected_result=self.error_message_listing_sub_venue,
                        actual_result=error_response_step_4)
        # endregion, step 4

        # region step 5, create Risk limit Dimension rule without impossible combination Listing Group + Venue
        parameters_step_5 = {
            "riskLimitDimensionName": self.rules_name[4],
            "riskLimitDimensionDesc": self.rules_name[4],
            "riskLimitDimensionExp": "test",
            "venueID": self.risk_limit_dimensions['venueID'],
            "listingGroupID": self.risk_limit_dimensions['listingGroupID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_5)
        error_response_step_5 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: ListingGroup + Venue",
                        expected_result=self.error_message_listing_group_venue,
                        actual_result=error_response_step_5)
        # endregion, step 5

        # region step 6, create Risk limit Dimension rule without impossible combination Listing Group + Sub Venue
        parameters_step_6 = {
            "riskLimitDimensionName": self.rules_name[5],
            "riskLimitDimensionDesc": self.rules_name[5],
            "riskLimitDimensionExp": "test",
            "subVenueID": self.risk_limit_dimensions['subVenueID'],
            "listingGroupID": self.risk_limit_dimensions['listingGroupID']
        }
        self.risk_limit_dimension_message.create_risk_limit_dimension(custom_params=parameters_step_6)
        error_response_step_6 = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.risk_limit_dimension_message))
        data_validation(test_id=self.test_id,
                        event_name="Impossible combinations: ListingGroup + SubVenue",
                        expected_result=self.error_message_listing_group_sub_venue,
                        actual_result=error_response_step_6)
        # endregion, step 6
