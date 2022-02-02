from enum import Enum

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiCommissionsMessages(RestApiMessages):

    def __init__(self, data_set: BaseDataSet, message_type: str = ''):
        super().__init__(message_type)
        self.data_set = data_set

    def clear_fees_request(self, fee: Enum):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': fee.name,
            'commissionID': fee.value,
            'miscFeeType': self.data_set.get_misc_fee_type_by_name("exch_fees")
        }
        self.parameters = default_parameters

    def modify_fees_request(self, params=None, recalculate=False, fee: Enum = None, comm_profile: str = None,
                            fee_type: str = None):
        self.message_type = 'ModifyCommission'
        exch_fees = self.data_set.get_misc_fee_type_by_name("exch_fees")
        default_comm_profile = self.data_set.get_comm_profile_by_name("abs_amt")
        default_fee = self.data_set.get_fee_by_name("fee1")
        default_parameters = {
            'commDescription': default_fee.name if fee is None else fee.name,
            'commExecScope': self.data_set.get_fee_exec_scope_by_name("all_exec"),
            'commissionID': default_fee.value if fee is None else fee.value,
            'execCommissionProfileID': default_comm_profile if comm_profile is None else comm_profile,
            'miscFeeType': exch_fees if fee_type is None else fee_type,
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        self.parameters = params if params is not None else default_parameters

    def modify_client_commission_request(self, params=None, client: str = None, account: str = None, recalculate=False,
                                         commission: Enum = None, comm_profile: str = None):
        default_client = self.data_set.get_client_by_name("client_com_1")
        default_comm_profile = self.data_set.get_comm_profile_by_name("abs_amt")
        default_commission = self.data_set.get_commission_by_name("commission1")
        self.message_type = 'ModifyClCommission'
        default_parameters = {
            'accountGroupID': default_client if client is None else client,
            'clCommissionID': default_commission.value if commission is None else commission.value,
            'clCommissionName': default_commission.name if commission is None else commission.name,
            'commissionAmountType': "BRK",
            'commissionProfileID': default_comm_profile if comm_profile is None else comm_profile,
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        if account is not None and client is None:
            default_parameters.pop("accountGroupID")
            default_parameters["accountID"] = account
        self.parameters = params if params is not None else default_parameters

    def clear_commissions_request(self, commission: Enum = None):
        self.message_type = 'ModifyClCommission'
        default_commission = self.data_set.get_commission_by_name("commission1")
        default_parameters = {
            'clCommissionID': default_commission.value if commission is None else commission.value,
            'clCommissionName': default_commission.name if commission is None else commission.name,
            'recomputeInConfirmation': 'false',
            'commissionAmountType': "BRK"
        }
        self.parameters = default_parameters
