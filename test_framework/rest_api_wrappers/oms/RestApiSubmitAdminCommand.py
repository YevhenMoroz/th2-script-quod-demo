from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiSubmitAdminCommandBlock(RestApiMessages):
    def __init__(self):
        super().__init__("submitAdminCommand")

    def set_default_param(self, component: str, adm_command: str, admin_comm_param_name: str, admin_comm_param_value: str):
        params = {
            "componentID": component,
            "adminCommand": adm_command,
            "adminCommandParam": [
                {
                    "adminCommandParamName": admin_comm_param_name,
                    "adminCommandParamValue": admin_comm_param_value
                }
            ]
        }
        self.set_params(params)
        return self

