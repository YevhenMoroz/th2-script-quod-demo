from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiCashAccountMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_cash_account_counters(self, client_name, currency):
        self.message_type = "FindCashAccountCounters"
        self.parameters = {'URI': {
            "queryID": client_name,
            "queryID2": currency
        }}