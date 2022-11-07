from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiWashBookMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_security_account_wash_book(self):
        self.message_type = "FindAllSecurityAccountWashBook"

    def create_security_account(self, custom_params=None, wash_book_name=None, institution_id=None):
        self.message_type = "CreateSecurityAccount"
        default_parameters = {
            "accountID": wash_book_name,
            "accountDesc": wash_book_name,
            "clientAccountID": wash_book_name,
            "clientAccountIDSource": "BIC",
            "isWashBook": "true",
            "institutionID": institution_id,
            "alive": "true"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

    def enable_security_account(self, account_id):
        self.message_type = "EnableSecurityAccount"
        self.parameters = {
            "accountID": account_id
        }

    def disable_security_account(self, account_id):
        self.message_type = "DisableSecurityAccount"
        self.parameters = {
            "accountID": account_id
        }

