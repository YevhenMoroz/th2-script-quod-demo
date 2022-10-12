from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyGatingRuleMessage(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("ModifyGatingRule", data_set)
        self.base_parameters = {"accountGroupID": self.data_set.get_client_by_name("client_1"),
                                "gatingRuleDescription": "for regression",
                                "gatingRuleName": "GTRULE_RECOVERY",
                                "gatingRuleID": 800024,
                                "alive": "true",
                                "gatingRuleCondition": [
                                    {"gatingRuleCondExp": "AND(ExecutionPolicy=DMA,OrdQty<1000)",
                                     "gatingRuleCondName": "Cond1",
                                     "holdOrder": "false",
                                     "qtyPrecision": 100,
                                     "alive": "true",
                                     "gatingRuleCondIndice": 1,
                                     "gatingRuleResult": [
                                         {"alive": "true",
                                          "gatingRuleResultIndice": 1,
                                          "splitRatio": 1,
                                          "gatingRuleResultAction": "DMA",
                                          "gatingRuleResultRejectType": "HRD"}]},
                                    {"gatingRuleCondName": "Default Result",
                                     "alive": "true",
                                     "gatingRuleCondIndice": 2,
                                     "gatingRuleResult": [
                                        {"alive": "true",
                                         "gatingRuleResultIndice": 1,
                                         "splitRatio": 1,
                                         "gatingRuleResultAction": "DMA"}]}]}

    def set_default_param(self):
        self.set_params(self.base_parameters)
        return self
