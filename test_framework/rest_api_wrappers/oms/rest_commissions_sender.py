import time
from enum import Enum

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from test_framework.rest_api_wrappers.oms.RestApiCommissionsMessages import RestApiCommissionsMessages


class RestCommissionsSender(RestApiManager):

    def __init__(self, session_alias, case_id, data_set: BaseDataSet):
        super().__init__(session_alias, case_id)
        self.data_set = data_set
        self.message = RestApiCommissionsMessages(self.data_set)

    def clear_fees(self):
        fees = self.data_set.get_fees()
        for fee in fees:
            self.set_clear_fees_message(fee)
            self.send_post_request(self.message)
        time.sleep(2)
        return self

    def send_default_fee(self):
        self.set_modify_fees_message().change_message_params({"venueID": self.data_set.get_venue_by_name("venue_2")})
        self.send_post_request()

    def clear_commissions(self):
        commissions = self.data_set.get_commissions()
        for commission in commissions:
            self.set_clear_commissions_message(commission)
            self.send_post_request(self.message)
        return self

    def send_post_request(self, api_message: RestApiMessages = None):
        if api_message is None:
            api_message = self.message
        super().send_post_request(api_message)
        time.sleep(2)

    def set_clear_fees_message(self, fee: Enum):
        self.message.clear_fees_request(fee)
        return self

    def set_modify_fees_message(self, params=None, recalculate=False, fee: Enum = None,
                                comm_profile: str = None, fee_type: str = None):
        self.message.modify_fees_request(params, recalculate, fee, comm_profile, fee_type)
        return self

    def set_modify_client_commission_message(self, params=None, client: str = None, account: str = None,
                                             recalculate=False, commission: Enum = None, comm_profile: str = None):
        self.message.modify_client_commission_request(params, client, account, recalculate, commission, comm_profile)
        return self

    def set_clear_commissions_message(self, commission: Enum = None):
        self.message.clear_commissions_request(commission)
        return self

    def change_message_params(self, params):
        self.message.change_params(params)
        return self

    def remove_parameter(self, parameter_name):
        self.message.remove_parameter(parameter_name)
