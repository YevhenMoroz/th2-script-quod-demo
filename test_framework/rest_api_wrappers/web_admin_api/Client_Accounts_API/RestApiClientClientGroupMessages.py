from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiClientClientGroupMessages(WebAdminRestApiMessages):

    def create_client_client_group(self, custom_params=None):
        self.message_type = "CreateClientClientGroup"
        default_parameters = {
            "clientClientGroupID": "api_client_client_group",
            "clientGroupID": 1
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters
