from test_framework.fix_wrappers.DataSet import Fees, Commissions, CommissionProfiles, FeeTypes, CommissionClients, \
    CommissionAccounts
from test_framework.rest_api_wrappers.oms.RestApiCommissionsMessages import RestApiCommissionsMessages
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestCommissionsSender(RestApiManager):

    def __init__(self, session_alias, case_id):
        super().__init__(session_alias, case_id)
        self.message = RestApiCommissionsMessages()

    def clear_fees(self):
        self.set_clear_fees_message(Fees.Fee1)
        self.send_post_request(self.message)
        self.set_clear_fees_message(Fees.Fee2)
        self.send_post_request(self.message)
        self.set_clear_fees_message(Fees.Fee3)
        self.send_post_request(self.message)
        return self

    def send_default_fee(self):
        self.set_modify_fees_message().change_message_params({"venueID": "EUREX"})
        self.send_post_request()

    def clear_commissions(self):
        self.set_clear_commissions_message(Commissions.Commission1)
        self.send_post_request(self.message)
        self.set_clear_commissions_message(Commissions.Commission2)
        self.send_post_request(self.message)
        self.set_clear_commissions_message(Commissions.Commission3)
        self.send_post_request(self.message)
        return self

    def send_post_request(self, api_message: RestApiMessages = None):
        if api_message is None:
            api_message = self.message
        super().send_post_request(api_message)

    def set_clear_fees_message(self, fee: Fees):
        self.message.clear_fees_request(fee)
        return self

    def set_modify_fees_message(self, params=None, recalculate=False, fee: Fees = None,
                                comm_profile: CommissionProfiles = None, fee_type: FeeTypes = None):
        self.message.modify_fees_request(params, recalculate, fee, comm_profile, fee_type)
        return self

    def set_modify_client_commission_message(self, params=None, client: CommissionClients = None,
                                             account: CommissionAccounts = None, recalculate=False,
                                             commission: Fees = None,
                                             comm_profile: CommissionProfiles = None):
        self.message.modify_client_commission_request(params, client, account, recalculate, commission, comm_profile)
        return self

    def set_clear_commissions_message(self, commission: Commissions = None):
        self.message.clear_commissions_request(commission)
        return self

    def change_message_params(self, params):
        self.message.change_params(params)
        return self
