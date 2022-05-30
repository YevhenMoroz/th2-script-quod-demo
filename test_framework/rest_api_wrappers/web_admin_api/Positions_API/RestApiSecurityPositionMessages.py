from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiSecurityPositionMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_positions(self, security_account_name, alive=False):
        self.message_type = "FindPositions"
        self.parameters = {'URI': {
            "queryLookup": security_account_name,
            "aliveOnly": alive
        }}

    def modify_security_positions(self, params):
        self.message_type = "ModifyPosition"
        self.parameters = params
