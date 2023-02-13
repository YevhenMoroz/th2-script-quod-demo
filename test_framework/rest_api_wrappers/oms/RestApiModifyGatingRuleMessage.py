from copy import deepcopy

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyGatingRuleMessage(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("ModifyGatingRule", data_set)
        self.base_parameters = {"gatingRuleDescription": "for regression",
                                "gatingRuleName": "Main Rule",
                                "gatingRuleID": 2200035,
                                "alive": "true",
                                "mainGatingRule": "true",
                                "gatingRuleCondition": [
                                    {"gatingRuleCondExp": "VenueID=CS",
                                     "gatingRuleCondName": "All Orders",
                                     "alive": "true",
                                     "gatingRuleCondIndice": 1,
                                     "gatingRuleResult": [
                                         {"alive": "true",
                                          "gatingRuleResultIndice": 1,
                                          "splitRatio": 1,
                                          "gatingRuleResultAction": "ORI",
                                          "holdOrder": 'false'}]},
                                    {"gatingRuleCondName": "Default Result",
                                     "gatingRuleCondIndice": 2,
                                     "gatingRuleResult": [
                                        {
                                         "alive":"true",
                                         "gatingRuleResultIndice": 1,
                                         "splitRatio": 1,
                                         "holdOrder": 'false',
                                         "gatingRuleResultAction": "ORI"}]}]}

    def set_default_param(self):
        self.set_params(deepcopy(self.base_parameters))
        return self
