import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_cases.wrapper.ret_wrappers import verifier
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_6295(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_washbook_rule_message = RestApiWashBookRuleMessages(data_set=data_set)
        self.api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)

    @staticmethod
    def check_washbook_rule_status(response, tested_washbook_rule_name, test_id):

        washbook_rule_status = True
        for count in range(len(response)):
            rule_name = response[count]["washBookRuleName"]
            if rule_name == tested_washbook_rule_name:
                bca.create_event(f'Fail test event, {tested_washbook_rule_name} is present on the Web Admin',
                                 status='FAILED',
                                 parent_id=test_id)
                washbook_rule_status = False
                break
        if washbook_rule_status:
            bca.create_event(f'Passed test event, {tested_washbook_rule_name} is not present on the Web Admin',
                             status='SUCCESS',
                             parent_id=test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create new WashBookRule and Verify response - step 1
        self.api_washbook_rule_message.create_washbook_rule()
        self.api_manager.send_post_request(self.api_washbook_rule_message)

        self.api_washbook_rule_message.find_all_washbook_rule()
        parsed_response = self.api_manager.parse_response_details(
            response=self.api_manager.send_get_request(self.api_washbook_rule_message),
            filter_dict={'washBookRuleName': self.api_washbook_rule_message.default_washbook_rule})
        try:
            verifier(case_id=self.test_id,
                     event_name="Check WashBookRule status",
                     expected_value="true",
                     actual_value=parsed_response['alive'])
            rule_id = parsed_response[0]["washBookRuleID"]
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion

        # region Modify created WashBookRule and Verify response - step 2
        print(parsed_response)



# def execute(report_id):
#     case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
#
#
#     # region Modify created WashBookRule and Verify response - step 2
#     modify_wash_book_rule_params = {
#         'washBookRuleID': rule_id,
#         "washBookRuleName": tested_wash_book_name,
#         "instrType": "EQU",
#         "washBookAccountID": "HAKKIM3",
#         "institutionID": 1
#     }
#
#     print(modify_wash_book_rule_params['washBookRuleID'])
#     api_message.modify_wash_book_rule(modify_wash_book_rule_params)
#     api_manager.send_post_request(api_message)
#
#     api_message.find_all_wash_book_rule()
#     modified_rule_params = api_manager.get_response_details(
#         response=api_manager.send_get_request(api_message),
#         response_name=response_name,
#         expected_entity_name=modify_wash_book_rule_params['washBookRuleID'],
#         entity_field_id="washBookRuleID")
#     print(modified_rule_params)
#     try:
#         verifier(case_id=case_id,
#                  event_name="Check new field for WashBookRule ",
#                  expected_value="EQU",
#                  actual_value=modified_rule_params['instrType'].simple_value)
#     except:
#         bca.create_event(f'Fail test event. Response is empty',
#                          status='FAILED',
#                          parent_id=case_id)
#     # endregion
#
#     # region Delete WashBookRule - step 3
#     api_message.delete_wash_book_rule(wash_book_rule_id=rule_id)
#     api_manager.send_post_request(api_message)
#
#     api_message.find_all_wash_book_rule()
#     try:
#         response = api_manager.send_get_request(api_message)
#         for count in range(len(response.fields[response_name].list_value.values)):
#             entity = response.fields[response_name].list_value.values[count].message_value.fields[
#                 "washBookRuleName"].simple_value
#             if entity == tested_wash_book_name:
#                 bca.create_event(f'Fail test event, {tested_wash_book_name} not deleted on the Web Admin',
#                                  status='FAILED',
#                                  parent_id=case_id)
#                 break
#     except:
#         bca.create_event(f'Fail test event. Response is empty',
#                          status='FAILED',
#                          parent_id=case_id)
    # endregion
