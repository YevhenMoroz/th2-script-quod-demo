from copy import deepcopy
from enum import Enum

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiSettlementModelMessages(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("", data_set)
        self.message_type = "ModifySettlementModel"
        self.base_parameters = {
            "instrType": 'EQU',
            "settlLocationBIC": 'TESTBIC',
            "settlLocationID": '2',
            "settlementModelDescription": 'PSET to test',
            "settlementModelID": '3',
            "settlementModelName": "Test PSET"
        }

    def set_modify_message_amend(self, account_group_id, venue_id):
        parameters = deepcopy(self.base_parameters)
        parameters.update({"accountGroupID": account_group_id, "venueID": venue_id})
        self.parameters = parameters

    def set_modify_message_clear(self):
        self.parameters = self.base_parameters
