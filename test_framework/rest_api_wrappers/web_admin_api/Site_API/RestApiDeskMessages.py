from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiDeskMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_desk(self):
        self.message_type = "FindAllDesk"

    def create_desk(self, custom_params):
        self.message_type = "CreateDesk"
        self.parameters = custom_params

    def modify_desk(self, custom_params):
        self.message_type = "ModifyDesk"
        self.parameters = custom_params

    def enable_desk(self):
        pass

    def disable_desk(self):
        pass
