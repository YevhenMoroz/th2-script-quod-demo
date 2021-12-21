from test_framework.fix_wrappers.DataSet import Fees, CommissionClients, CommissionAccounts, \
    CommissionProfiles, Commissions
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestCommissionsSender(RestApiManager):

    def __init__(self, session_alias, case_id):
        super().__init__(session_alias, case_id)
        self.message = RestApiMessages()

    def change_params(self, param_modify: dict):
        for key, value in param_modify.items():
            self.message.parameters[key] = value
        return self

    def clear_fees(self):
        self.clear_fees_request(Fees.Fee1)
        self.send_post_request(self.message)
        self.clear_fees_request(Fees.Fee2)
        self.send_post_request(self.message)
        self.clear_fees_request(Fees.Fee3)
        self.send_post_request(self.message)
        return self

    def send_default_fee(self):
        self.modify_fees_request().change_params({"venueID": "EUREX"}).send_post_request()

    def clear_fees_request(self, fee: Fees):
        self.message.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': fee.name,
            'commissionID': fee.value,
            'miscFeeType': 'EXC'
        }
        self.message.parameters = default_parameters
        return self

    def modify_fees_request(self, params=None, recalculate=False, fee: Fees = None,
                            comm_profile: CommissionProfiles = None):
        self.message.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': "Fee1" if fee is None else fee.name,
            'commExecScope': "ALL",
            'commissionID': 1 if fee is None else fee.value,
            'execCommissionProfileID': 1 if comm_profile is None else comm_profile.value,
            'miscFeeType': 'EXC',
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        self.message.parameters = params if params is not None else default_parameters
        return self

    def modify_client_commission_request(self, params=None, client: Commissions = None,
                                         account: CommissionAccounts = None, recalculate=False,
                                         commission: Fees = None,
                                         comm_profile: CommissionProfiles = None):
        self.message.message_type = 'ModifyClCommission'
        default_parameters = {
            'accountGroupID': "CLIENT_COMM_1" if client is None else client.value,
            'clCommissionID': 1 if commission is None else commission.value,
            'clCommissionName': "Commission1" if commission is None else commission.name,
            'commissionAmountType': "BRK",
            'commissionProfileID': 1 if comm_profile is None else comm_profile.value,
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        if account is not None and client is None:
            default_parameters.pop("accountGroupID")
            default_parameters["accountID"] = account.value
        self.message.parameters = params if params is not None else default_parameters
        return self

    def clear_commissions_request(self, commission: Commissions = None):
        self.message.message_type = 'ModifyClCommission'
        default_parameters = {
            'clCommissionID': 1 if commission is None else commission.value,
            'clCommissionName': "Commission1" if commission is None else commission.name,
            'recomputeInConfirmation': 'false',
            'commissionAmountType': "BRK"
        }
        self.message.parameters = default_parameters
        return self

    def clear_commissions(self):
        self.clear_commissions_request(Commissions.Commission1)
        self.send_post_request(self.message)
        self.clear_commissions_request(Commissions.Commission2)
        self.send_post_request(self.message)
        self.clear_commissions_request(Commissions.Commission3)
        self.send_post_request(self.message)
        return self

    def send_post_request(self, api_message: RestApiMessages = None):
        if api_message is None:
            api_message = self.message
        super().send_post_request(api_message)
