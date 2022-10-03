from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiCumTradingLimitCounter(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_cum_trading_limit_counters(self):
        self.message_type = "FindAllCumTradingLimitCounter"

    def create_cum_trading_limit_counter(self, custom_params=None):
        pass

    def modify_cum_trading_limit_counter(self, params):
        self.message_type = "ModifyCumTradingLimitCounter"
        self.parameters = params

