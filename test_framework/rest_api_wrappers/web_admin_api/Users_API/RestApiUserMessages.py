from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet

class RestApiUserMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_user(self):
        self.message_type = "FindAllUser"

    def modify_user(self, params):
        self.message_type = "ModifyUser"
        self.parameters = params