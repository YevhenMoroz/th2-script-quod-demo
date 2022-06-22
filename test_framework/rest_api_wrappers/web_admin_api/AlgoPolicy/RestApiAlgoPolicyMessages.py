from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet

class RestApiAlgoPolicyMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_algo_policies(self):
        self.message_type = "FindAllAlgoPolicy"

    def modify_algo_policy(self, parameters):
        self.message_type = "ModifyAlgoPolicy"
        self.parameters = parameters






