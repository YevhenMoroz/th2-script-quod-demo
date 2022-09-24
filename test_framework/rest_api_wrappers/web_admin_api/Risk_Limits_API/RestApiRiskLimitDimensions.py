from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiRiskLimitDimensions(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_risk_limit_dimension(self):
        self.message_type = "FindAllRiskLimitDimensions"

    def create_risk_limit_dimension(self, custom_params=None):
        self.message_type = "CreateRiskLimitDimension"
        self.parameters = custom_params

    def modify_risk_limit_dimension(self, params):
        self.message_type = "ModifyRiskLimitDimension"
        self.parameters = params

    def delete_risk_limit_dimension(self, risk_limit_dimension_id):
        self.message_type = "DeleteRiskLimitDimension"
        delete_params = {
            "riskLimitDimensionID": risk_limit_dimension_id
        }
        self.parameters = delete_params
