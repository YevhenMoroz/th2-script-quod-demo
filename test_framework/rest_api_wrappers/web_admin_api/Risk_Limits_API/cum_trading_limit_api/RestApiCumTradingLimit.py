from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiCumTradingLimit(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_cum_trading_limit_rules(self):
        self.message_type = "FindAllCumTradingLimit"

    def create_cum_trading_limit_rule(self, custom_params=None):
        self.message_type = "CreateCumTradingLimit"
        self.parameters = custom_params

    def modify_cum_trading_limit_rule(self, params):
        self.message_type = "ModifyCumTradingLimit"
        self.parameters = params

