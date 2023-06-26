from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiGatingRuleMessages(RestApiMessages):

    def set_main_rule(self):
        self.parameters = {
            "alive": "true",
            "gatingRuleCondition": [
                {"alive": "true", "gatingRuleCondExp": "InstrSymbol=EUR/CAD", "gatingRuleCondIndice": 1,
                 "gatingRuleCondName": "First Main",
                 "gatingRuleResult": [{"alive": "true", "gatingRuleResultAction": "REJ",
                                       "gatingRuleResultIndice": 1, "holdOrder": "false",
                                       "priceOrigin": "PAR", "splitRatio": 1, "venueID": "BARX",
                                       "gatingRuleResultRejectType": "HRD"}]},
                {"alive": "true", "gatingRuleCondIndice": 2,
                 "gatingRuleCondName": "Default Result",
                 "gatingRuleResult": [{"alive": "true", "gatingRuleResultAction": "ORI",
                                       "gatingRuleResultIndice": 1, "holdOrder": "false",
                                       "priceOrigin": "PAR", "splitRatio": 1}]},
                ],
            "gatingRuleID": 3000015,
            "gatingRuleName": "Main Rule"
        }
        return self

    def set_secondary_rule(self):
        self.parameters = {
            "alive": "true",
            "gatingRuleCondition": [
                {"alive": "true", "gatingRuleCondExp": "AND(InstrSymbol=EUR/CAD,VenueID=GS)", "gatingRuleCondIndice": 1,
                 "gatingRuleCondName": "DMA",
                 "gatingRuleResult": [{"alive": "true", "gatingRuleResultAction": "DMA",
                                       "gatingRuleResultIndice": 1, "holdOrder": "false",
                                       "priceOrigin": "PAR", "splitRatio": 1, "venueID": "BARX"}]},
                {"alive": "true", "gatingRuleCondExp": "OrdQty>2000000", "gatingRuleCondIndice": 2,
                 "gatingRuleCondName": "Trigger GT",
                 "gatingRuleResult": [{"alive": "true", "gatingRuleResultAction": "REJ",
                                       "gatingRuleResultIndice": 1, "gatingRuleResultRejectType": "HRD",
                                       "holdOrder": "false", "splitRatio": 1}]},
                ],
            "gatingRuleID": 3800024,
            "gatingRuleName": "Automation_secondary_rule"
        }
        return self

    def modify_gating_rule(self):
        self.message_type = 'ModifyGatingRule'
        return self

    def enable_gating_rule(self):
        self.message_type = 'EnableGatingRule'
        self.change_params({"alive": "false"})
        temp = self.get_parameters()["gatingRuleCondition"]
        for index, instance in enumerate(temp):
            instance.update({"alive": "false"})
            instance["gatingRuleResult"][0].update({"alive": "false"})
            temp[index].update(instance)
        return self

    def disable_gating_rule(self):
        self.message_type = 'DisableGatingRule'
        self.change_params({"alive": "true"})
        temp = self.get_parameters()["gatingRuleCondition"]
        for index, instance in enumerate(temp):
            instance.update({"alive": "true"})
            instance["gatingRuleResult"][0].update({"alive": "true"})
            temp[index].update(instance)
        return self
