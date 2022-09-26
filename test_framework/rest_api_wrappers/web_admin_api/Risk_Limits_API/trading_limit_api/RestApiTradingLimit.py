from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiTradingLimit(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_trading_limit_rules(self):
        self.message_type = "FindAllTradingLimit"

    def create_trading_limit_rule(self, custom_params=None):
        self.message_type = "CreateTradingLimit"
        self.parameters = custom_params

    def modify_trading_limit_rule(self, params):
        self.message_type = "ModifyTradingLimit"
        self.parameters = params

