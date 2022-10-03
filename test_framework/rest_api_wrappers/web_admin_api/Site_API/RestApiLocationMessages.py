from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiLocationMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_location(self):
        self.message_type = "FindAllLocation"

    def create_location(self, custom_params):
        self.message_type = "CreateLocation"
        self.parameters = custom_params

    def modify_location(self, custom_params):
        self.message_type = "ModifyLocation"
        self.parameters = custom_params

    def enable_location(self):
        pass

    def disable_location(self):
        pass
