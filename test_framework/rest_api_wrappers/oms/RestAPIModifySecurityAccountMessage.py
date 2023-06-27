from copy import deepcopy

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from test_framework.rest_api_wrappers.oms.VenueSecActNameEntity import VenueSecActNameEntity


class RestAPIModifySecurityAccountMessage(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("", data_set)
        self.message_type = "ModifySecurityAccount"
        self.default_parameters = {"accountGroupID": "CLIENT_REST_API",
                                   "accountDesc": "Account for CLIENT_REST_API",
                                   "clientAccountID": self.data_set.get_account_by_name('client_rest_api_acc_2'),
                                   "accountID": "CLIENT_REST_API_SA2",
                                   "clientAccountIDSource": "OTH",
                                   "clearingAccountType": "INS",
                                   "isWashBook": 'false',
                                   "clientMatchingID": "CLIENT_REST_API_SA2",
                                   "tradeConfirmEligibility": 'false',
                                   "alive": 'true'}

    def set_default(self):
        self.parameters.update(deepcopy(self.default_parameters))

    def add_additional_parameters(self, parameters):
        self.parameters.update(parameters)
