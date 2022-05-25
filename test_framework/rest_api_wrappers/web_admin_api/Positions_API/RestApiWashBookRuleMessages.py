from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiWashBookRuleMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)
        self.default_washbook_rule = self.data_set.get_washbook_rule_by_name('washbook_rule_1')
        self.default_washbook_name = self.data_set.get_washbook_account_by_name('washbook_account_1')

    def find_all_washbook_rule(self):
        self.message_type = "FindAllWashBookRule"

    def create_washbook_rule(self, custom_params=None):
        self.message_type = "CreateWashBookRule"
        default_parameters = {
            "washBookRuleName": self.default_washbook_rule,
            "washBookAccountID": self.default_washbook_name,
            "institutionID": 1
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

    def modify_wash_book_rule(self, params):
        self.message_type = "ModifyWashBookRule"
        self.parameters = params

    def delete_washbook_rule(self, washbook_rule_id):
        self.message_type = "DeleteWashBookRule"
        delete_params = {
            'washBookRuleID': int(washbook_rule_id),
        }
        self.parameters = delete_params
