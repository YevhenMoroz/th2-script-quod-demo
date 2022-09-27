from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiClientGroupMessages(WebAdminRestApiMessages):

    def create_client_list(self, custom_params=None):
        self.message_type = "CreateClientGroup"
        default_parameters = {
            "clientGroupName": "api_client_group"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters
