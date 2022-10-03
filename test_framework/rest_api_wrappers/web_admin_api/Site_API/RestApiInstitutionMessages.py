from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiInstitutionMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_institution(self):
        self.message_type = "FindAllInstitution"

    def create_institution(self, custom_params=None):
        self.message_type = "CreateInstitution"
        default_parameters = {
            "institutionName": "api_institution"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

    def modify_institution(self, custom_params):
        self.message_type = "ModifyInstitution"
        self.parameters = custom_params

    def enable_institution(self):
        pass

    def disable_institution(self):
        pass
