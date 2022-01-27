from test_framework.fix_wrappers.DataSet import Fees, FeeTypes, CommissionProfiles, ExecScope, CommissionAccounts, \
    CommissionClients, Commissions
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiCommissionsMessages(RestApiMessages):

    def clear_fees_request(self, fee: Fees):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': fee.name,
            'commissionID': fee.value,
            'miscFeeType': FeeTypes.ExchFees.value
        }
        self.parameters = default_parameters

    def modify_fees_request(self, params=None, recalculate=False, fee: Fees = None,
                            comm_profile: CommissionProfiles = None, fee_type: FeeTypes = None):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': "Fee1" if fee is None else fee.name,
            'commExecScope': ExecScope.AllExec.value,
            'commissionID': 1 if fee is None else fee.value,
            'execCommissionProfileID': 1 if comm_profile is None else comm_profile.value,
            'miscFeeType': FeeTypes.ExchFees.value if fee_type is None else fee_type.value,
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        self.parameters = params if params is not None else default_parameters

    def modify_client_commission_request(self, params=None, client: CommissionClients = None,
                                         account: CommissionAccounts = None, recalculate=False,
                                         commission: Fees = None,
                                         comm_profile: CommissionProfiles = None):
        self.message_type = 'ModifyClCommission'
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
        self.parameters = params if params is not None else default_parameters

    def clear_commissions_request(self, commission: Commissions = None):
        self.message_type = 'ModifyClCommission'
        default_parameters = {
            'clCommissionID': 1 if commission is None else commission.value,
            'clCommissionName': "Commission1" if commission is None else commission.name,
            'recomputeInConfirmation': 'false',
            'commissionAmountType': "BRK"
        }
        self.parameters = default_parameters

    def change_params(self, param_modify: dict):
        for key, value in param_modify.items():
            self.parameters[key] = value
