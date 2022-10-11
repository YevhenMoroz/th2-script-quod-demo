import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiWashBookRuleMessages import \
    RestApiWashBookRuleMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3488(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.washbook_rule_message = RestApiWashBookRuleMessages(data_set=data_set)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.wash_book_rule_id = 0

    @staticmethod
    def check_washbook_rule_status(response, tested_washbook_rule_id, test_id):
        try:
            washbook_rule_status = True
            for count in range(len(response)):
                rule_name = response[count]["washBookRuleID"]
                if rule_name == tested_washbook_rule_id:
                    bca.create_event(f'Fail test event, WashBookRule with ID={tested_washbook_rule_id}'
                                     f'is present on the Web Admin',
                                     status='FAILED',
                                     parent_id=test_id)
                    washbook_rule_status = False
                    break
            if washbook_rule_status:
                bca.create_event(f'Passed test event, WashBookRule with ID={tested_washbook_rule_id}'
                                 f' is not present on the Web Admin',
                                 status='SUCCESS',
                                 parent_id=test_id)
        except(KeyError, TypeError, IndexError):
            bca.create_event('Fail test event. Response is empty.', status='FAILED', parent_id=test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create new WashBookRule and Verify response - step 1
        self.washbook_rule_message.create_washbook_rule()
        self.wa_api_manager.send_post_request(self.washbook_rule_message)

        self.washbook_rule_message.find_all_washbook_rule()
        wash_book_rule = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.washbook_rule_message),
            filter_dict={'washBookRuleName': self.washbook_rule_message.default_washbook_rule})
        try:
            data_validation(test_id=self.test_id,
                            event_name="Check WashBookRule status",
                            expected_result="true",
                            actual_result=wash_book_rule[0]['alive'])
            self.wash_book_rule_id = wash_book_rule[0]["washBookRuleID"]
        except(KeyError, TypeError, IndexError):
            bca.create_event(f'Step 1. Fail test event. Response is empty.', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Modify created WashBookRule and Verify response - step 2
        try:
            wash_book_rule[0].pop("alive")
            wash_book_rule[0].update({"instrType": "EQU"})
            wash_book_rule[0].update({"washBookRuleID": self.wash_book_rule_id})
            self.washbook_rule_message.modify_wash_book_rule(params=wash_book_rule[0])
            self.wa_api_manager.send_post_request(self.washbook_rule_message)

            self.washbook_rule_message.find_all_washbook_rule()
            modified_wash_book_rule = self.wa_api_manager.parse_response_details(
                response=self.wa_api_manager.send_get_request(self.washbook_rule_message),
                filter_dict={"washBookRuleID": self.wash_book_rule_id})
            data_validation(test_id=self.test_id,
                            event_name="Check that new WashBookRule field - instrType=EQU is present",
                            expected_result="EQU",
                            actual_result=modified_wash_book_rule[0]['instrType'])
        except(KeyError, TypeError, IndexError):
            bca.create_event(f'Step 2. Fail test event. Response is empty.', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Delete WashBookRule - step 3
        self.washbook_rule_message.delete_washbook_rule(washbook_rule_id=self.wash_book_rule_id)
        self.wa_api_manager.send_post_request(self.washbook_rule_message)

        self.washbook_rule_message.find_all_washbook_rule()
        wash_book_rules = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.washbook_rule_message))
        self.check_washbook_rule_status(wash_book_rules, self.wash_book_rule_id, self.test_id)
        # endregion
