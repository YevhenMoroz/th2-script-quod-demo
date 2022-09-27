from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiClientMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_client(self):
        self.message_type = "FindAllAccountGroup"

    def create_client(self, custom_params=None):
        self.message_type = "CreateAccountGroup"
        default_parameters = {
            "accountMgrUserID": self.data_set.get_recipient_by_name('recipient_user_2'),
            "accountGroupName": self.data_set.get_client_by_name('client_5'),
            "accountMgrDeskID": 1,
            "clientAccountGroupID": self.data_set.get_client_by_name('client_5'),
            "accountGroupID": self.data_set.get_client_by_name('client_5'),
            "accountType": "HT",
            "accountScheme": "S",
            "transactionType": "C",
            "discloseExec": "R",
            "accountMgrRoleID": "HSD",
            "clearingAccountType": "FIR",
            "allocationInst": "MAN"
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




