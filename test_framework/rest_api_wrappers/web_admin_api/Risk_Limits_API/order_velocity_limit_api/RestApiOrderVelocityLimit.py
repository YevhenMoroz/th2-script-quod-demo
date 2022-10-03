from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiOrderVelocityLimit(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_order_velocity_limit_rules(self):
        self.message_type = "FindAllOrderVelocityLimit"

    def create_order_velocity_limit_rule(self, custom_params=None):
        self.message_type = "CreateOrderVelocityLimit"
        self.parameters = custom_params

    def modify_order_velocity_limit_rule(self, params):
        self.message_type = "ModifyOrderVelocityLimit"
        self.parameters = params

