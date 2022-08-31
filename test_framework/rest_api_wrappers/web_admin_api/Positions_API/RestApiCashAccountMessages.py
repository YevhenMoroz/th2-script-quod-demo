from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiCashAccountMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_cash_account_counters(self, cash_account_id):
        self.message_type = "FindCashAccountCounters"
        self.parameters = {'URI': {
            "queryID": cash_account_id
        }}

    def create_cash_account(self, cash_account_name, currency, client):
        self.message_type = "CreateCashAccount"
        self.parameters = {
                "cashAccountName": cash_account_name,
                "venueCashAccountID": cash_account_name,
                "currency": currency,
                "accountGroupID": client,
                "clientCashAccountID": cash_account_name,
                "defaultCashAccount": "false",
                "alive": "true"
        }

    def modify_cash_account_transfer(self, cash_account_id, transfer_type, transfer_amount, free_notes="test"):
        self.message_type = "ModifyCashAccountTransfer"
        self.parameters = {
            "cashAccountID": cash_account_id,
            "cashActTransferType": transfer_type,
            "transferAmt": transfer_amount,
            "freeNotes": free_notes
        }
