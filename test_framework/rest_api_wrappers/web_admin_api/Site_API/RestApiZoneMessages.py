from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiZoneMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_zone(self):
        self.message_type = "FindAllZone"

    def create_zone(self, custom_params):
        self.message_type = "CreateZone"
        self.parameters = custom_params

    def modify_zone(self, custom_params):
        self.message_type = "ModifyZone"
        self.parameters = custom_params

    def enable_zone(self):
        pass

    def disable_zone(self):
        pass
