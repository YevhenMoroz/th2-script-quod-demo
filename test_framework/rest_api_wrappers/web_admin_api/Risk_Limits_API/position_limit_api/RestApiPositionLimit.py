from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiPositionLimit(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_position_limit_rules(self):
        self.message_type = "FindAllPositionLimit"

    def create_position_limit_rule(self, custom_params=None):
        self.message_type = "CreatePositionLimit"
        self.parameters = custom_params

    def modify_position_limit_rule(self, params):
        self.message_type = "ModifyPositionLimit"
        self.parameters = params

