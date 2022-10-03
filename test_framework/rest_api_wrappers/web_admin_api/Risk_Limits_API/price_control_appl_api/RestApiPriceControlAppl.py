from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiPriceControlAppl(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_price_control_appl_rules(self):
        self.message_type = "FindAllPriceControlAppl"

    def create_price_control_appl_rule(self, custom_params=None):
        self.message_type = "CreatePriceControlAppl"
        self.parameters = custom_params

    def modify_price_control_appl_rule(self, params):
        self.message_type = "ModifyPriceControlAppl"
        self.parameters = params

