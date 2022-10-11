from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiUserMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_user(self, user_id):
        self.message_type = "FindUser"
        self.parameters = {'URI': {
            "queryID": user_id
        }}

    def find_all_user(self):
        self.message_type = "FindAllUser"

    def create_user(self, custom_params):
        self.message_type = "CreateUser"
        self.parameters = custom_params

    def modify_user(self, custom_params):
        self.message_type = "ModifyUser"
        self.parameters = custom_params
