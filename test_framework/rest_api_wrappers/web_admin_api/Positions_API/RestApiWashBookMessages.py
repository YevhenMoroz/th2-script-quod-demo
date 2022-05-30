from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiWashBookMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)
        self.default_wash_book_account = self.data_set.get_washbook_account_by_name('washbook_account_3')

    def find_all_security_account_washBook(self):
        self.message_type = "FindAllSecurityAccountWashBook"

    def create_security_account(self, custom_params=None):
        self.message_type = "CreateSecurityAccount"
        default_parameters = {
            "accountID": self.default_wash_book_account,
            "accountDesc": self.default_wash_book_account,
            "clientAccountID": self.default_wash_book_account,
            "clientAccountIDSource": "BIC",
            "isWashBook": "true",
            "institutionID": 1,
            "alive": "true"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters


