import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserMessages import RestApiUserMessages
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import \
    RestApiInstitutionMessages
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.order_velocity_limit_api.RestApiOrderVelocityLimit import RestApiOrderVelocityLimit
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.utils.hierarchical_level_updater import hierarchical_level_updater


class QAP_T8623(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa_site = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.session_alias_wa_test = self.environment.get_list_web_admin_rest_api_environment()[1].session_alias_wa
        self.wa_api_manager_site = WebAdminRestApiManager(session_alias=self.session_alias_wa_site,
                                                          case_id=self.test_id)
        self.wa_api_manager_test = WebAdminRestApiManager(session_alias=self.session_alias_wa_test,
                                                          case_id=self.test_id)
        self.user_message = RestApiUserMessages(data_set=data_set)
        self.institution_message = RestApiInstitutionMessages(data_set=data_set)
        self.order_velocity_limit_message = RestApiOrderVelocityLimit(data_set=data_set)
        self.test_user = self.data_set.get_web_admin_rest_api_users_by_name('web_admin_rest_api_user_2')
        # RIN hierarchical level
        self.hierarchical_level_rin = self.data_set.get_hierarchical_level_by_name('hierarchical_level_1')
        self.institution_id_rin = self.hierarchical_level_rin['institutionID']
        # Test hierarchical level
        self.hierarchical_level_test = self.data_set.get_hierarchical_level_by_name('hierarchical_level_2')
        self.institution_id_test = self.hierarchical_level_test['institutionID']
        self.desk_id_test = self.hierarchical_level_test['deskID']['deskUserRole'][0]['deskID']
        self.order_velocity_limit_id = f'{self.qap_id}_api_rule_step2'
        self.error_message_step1 = "Request fails: code=QUOD-32533:Request not allowed:  HierarchicalLevel validations:" \
                                   " User adm_rest is not allowed to execute Adminmonitoring_OrderVelocityLimitCreationRequest"
        self.error_message_step2 = "Request fails: code=QUOD-32533:Request not allowed:  HierarchicalLevel validations:" \
                                   " User adm_rest is not allowed to execute Adminmonitoring_OrderVelocityLimitModificationRequest"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-Condition, set hierarchical level - Institution for test user and check result
        self.user_message.find_user(user_id=self.test_user)
        test_api_user = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))

        new_user_parameters = hierarchical_level_updater(test_id=self.test_id, user_response=test_api_user,
                                                         new_hierarchical_assignment=self.institution_id_test)
        self.user_message.modify_user(custom_params=new_user_parameters)
        self.wa_api_manager_site.send_post_request(self.user_message)

        self.user_message.find_user(user_id=self.test_user)
        test_api_user_pre_condition = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request_with_parameters(self.user_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Check that hierarchical level - 'Institution(id=3)' was set for '{self.test_user}' user.",
                        expected_result=self.institution_id_test['institutionID'],
                        actual_result=int(test_api_user_pre_condition[0]['institutionID']))
        # endregion

        # region step 1, Create 'OrderVelocityLimit' rule with 'Institution' which assigned to another hierarchical assignments
        parameters_step1 = {
            "orderVelocityLimitName": self.order_velocity_limit_id,
            "movingTimeWindow": 1,
            "institutionID": self.institution_id_rin['institutionID']
        }
        self.order_velocity_limit_message.create_order_velocity_limit_rule(custom_params=parameters_step1)
        create_order_velocity_limit_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.order_velocity_limit_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Create 'OrderVelocityLimit' rule with 'Institution'"
                                   f" which assigned to another hierarchical assignments.",
                        expected_result=self.error_message_step1,
                        actual_result=create_order_velocity_limit_response)
        # endregion

        # region step 2, Modify 'OrderVelocityLimit' rule with 'Institution' which assigned to another hierarchical assignments
        parameters_step2 = {
            "orderVelocityLimitName": self.order_velocity_limit_id,
            "movingTimeWindow": 1
        }
        self.order_velocity_limit_message.create_order_velocity_limit_rule(custom_params=parameters_step2)
        self.wa_api_manager_test.send_post_request(self.order_velocity_limit_message)

        self.order_velocity_limit_message.find_all_order_velocity_limit_rules()
        order_velocity_limit_rule = self.wa_api_manager_test.parse_response_details(
            response=self.wa_api_manager_test.send_get_request(self.order_velocity_limit_message),
            filter_dict={"orderVelocityLimitName": self.order_velocity_limit_id})
        data_validation(test_id=self.test_id,
                        event_name=f"Check that order velocity limit '{self.order_velocity_limit_id}' rule was created",
                        expected_result=self.order_velocity_limit_id,
                        actual_result=order_velocity_limit_rule[0]['orderVelocityLimitName'])
        order_velocity_limit_rule[0].update(self.institution_id_rin)
        order_velocity_limit_rule[0].pop('alive')
        self.order_velocity_limit_message.modify_order_velocity_limit_rule(params=order_velocity_limit_rule[0])
        modify_order_velocity_limit_response = self.wa_api_manager_test.parse_response_error_message_details(
            response=self.wa_api_manager_test.send_multiple_request(self.order_velocity_limit_message))
        data_validation(test_id=self.test_id,
                        event_name=f"Modify 'OrderVelocityLimit' rule with 'Institution'"
                                   f" which assigned to another hierarchical assignments.",
                        expected_result=self.error_message_step2,
                        actual_result=modify_order_velocity_limit_response)
        # endregion
