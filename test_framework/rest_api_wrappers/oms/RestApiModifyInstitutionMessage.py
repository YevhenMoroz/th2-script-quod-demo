from copy import deepcopy, copy

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyInstitutionMessage(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("", data_set)
        self.message_type = "ModifyInstitution"
        self.base_parameters = {
            'BIC': "QUODTESTGW3",
            'crossCurrencySettlement': True,
            'enableUnknownAccounts': False,
            "institutionID": 1,
            "institutionName": "QUOD FINANCIAL 1",
            "posFlatteningTime": 1658959200000,
            "settlCurrFxHairCut": 0,
            "settlCurrFxRateSource": "MAN"
        }

    def set_default_param(self):
        self.set_params(self.base_parameters)
        return self

    def modify_enable_unknown_accounts(self, value_of_modification: bool = False):
        self.update_parameters({'enableUnknownAccounts': value_of_modification})
