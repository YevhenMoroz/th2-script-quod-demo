from enum import Enum
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiWashBookRuleMessages(RestApiMessages):
    def __init__(self, data_set: BaseDataSet):
        super().__init__("")
        self.data_set = data_set
        self.default_washbook_rule_id = self.data_set.get_washbook_rule_by_name('RuleForTest')
        self.default_washbook_rule_name = 'RuleForTest'
        self.new_default_washbook_rule = self.data_set.get_washbook_rule_by_name('name_washbook_rule')
        self.default_washbook_account = self.data_set.get_washbook_account_by_name('washbook_account_4')

    def create_washbook_rule(self, washbook_rule_name: str = None, washbook_account: str = None,
                             institution_id: int = None, user: str = None, desk: str = None, instr_type: str = None,
                             exec_policy: str = None, client: str = None):
        self.message_type = "CreateWashBookRule"
        parameters = {
            "washBookRuleName": self.default_washbook_rule_name if washbook_rule_name is None else washbook_rule_name,
            "washBookAccountID": self.default_washbook_account if washbook_account is None else washbook_account,
            "institutionID": 1 if institution_id is None else institution_id
        }
        if user is not None:
            parameters.update({"userID": user})
        if desk is not None:
            parameters.update({"deskID": desk})
        if instr_type is not None:
            parameters.update({"instrType": instr_type})
        if exec_policy is not None:
            parameters.update({"executionPolicy": exec_policy})
        if client is not None:
            parameters.update({"accountGroupID": client})
        self.parameters = parameters

    def clear_washbook_rule(self):
        self.message_type = "ModifyWashBookRule"
        default_parameters = {
            "washBookRuleName": self.default_washbook_rule_name,
            "washBookRuleID": self.default_washbook_rule_id,
            "washBookAccountID": self.default_washbook_account,
            "institutionID": 1
        }
        self.parameters = default_parameters

    def modify_wash_book_rule(self, washbook_rule: Enum = None, washbook_account: Enum = None,
                              institution_id: int = None, user: str = None, desk: str = None, instr_type: str = None,
                             exec_policy: str = None, client: str = None, venue_list_id: int = None):
        self.message_type = "ModifyWashBookRule"
        parameters = {
            "washBookRuleName": self.default_washbook_rule_name if washbook_rule is None else washbook_rule.name,
            "washBookRuleID": self.default_washbook_rule_id if washbook_rule is None else washbook_rule.value,
            "washBookAccountID": self.default_washbook_account if washbook_account is None else washbook_account,
            "institutionID": 1 if institution_id is None else institution_id}
        if user is not None:
            parameters.update({"userID": user})
        if desk is not None:
            parameters.update({"deskID": desk})
        if instr_type is not None:
            parameters.update({"instrType": instr_type})
        if exec_policy is not None:
            parameters.update({"executionPolicy": exec_policy})
        if client is not None:
            parameters.update({"accountGroupID": client})
        if venue_list_id is not None:
            parameters.update({"venueListID": venue_list_id})
        self.parameters = parameters

    def delete_wash_book_rule(self, washbook_rule_id: int):
        self.message_type = "DeleteWashBookRule"
        delete_params = {
            'washBookRuleID': int(washbook_rule_id),
        }
        self.parameters = delete_params

    def disable_care_wash_book_rule(self):
        self.message_type = "ModifyWashBookRule"
        parameters = {
            "washBookRuleName": 'CARE Washbook',
            "washBookRuleID": 2,
            "washBookAccountID": 'CareWB',
            "institutionID": 1}
        self.parameters = parameters

    def enable_care_wash_book_rule(self):
        self.message_type = "ModifyWashBookRule"
        parameters = {
            "washBookRuleName": 'CARE Washbook',
            "washBookRuleID": 2,
            "washBookAccountID": 'CareWB',
            "institutionID": 1,
            "instrType": 'EQU',
            "executionPolicy": 'C'}
        self.parameters = parameters
