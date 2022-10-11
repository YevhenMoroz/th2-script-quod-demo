from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiClientListMessages(WebAdminRestApiMessages):

    def create_client_list(self, custom_params=None):
        self.message_type = "CreateClientList"
        default_parameters = {
            "clientListName": "api_client_list",
            "clientListDescription": "test"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters
