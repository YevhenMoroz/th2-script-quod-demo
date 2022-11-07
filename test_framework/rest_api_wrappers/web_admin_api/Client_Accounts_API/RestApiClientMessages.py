from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiClientMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_client(self):
        self.message_type = "FindAllAccountGroup"

    def create_client(self, client_name=None,  desk_id=None, custom_params=None):
        self.message_type = "CreateAccountGroup"
        default_parameters = {
            "accountGroupName": client_name,
            "managerDesk": desk_id,
            "clientAccountGroupID": client_name,
            "accountGroupID": client_name,
            "accountType": "HT",
            "accountScheme": "S",
            "transactionType": "C",
            "discloseExec": "R",
            "clearingAccountType": "FIR",
            "allocationInst": "MAN",
            "giveUpMatchingID": client_name
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

    def modify_client(self, parameters):
        self.message_type = "ModifyAccountGroup"
        self.parameters = parameters

    def enable_client(self, client_id):
        self.message_type = "EnableAccountGroup"
        self.parameters = {
            "accountGroupID": client_id,
        }

    def disable_client(self, client_id):
        self.message_type = "DisableAccountGroup"
        self.parameters = {
            "accountGroupID": client_id
        }




