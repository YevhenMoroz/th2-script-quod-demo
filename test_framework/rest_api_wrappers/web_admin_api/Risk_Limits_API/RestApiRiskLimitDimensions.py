from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet

class RestApiRiskLimitDimensions(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_risk_limit_dimension(self):
        pass

    def create_risk_limit_dimension(self):
        pass

    def modify_risk_limit_dimension(self):
        pass

    def delete_risk_limit_dimension(self):
        pass