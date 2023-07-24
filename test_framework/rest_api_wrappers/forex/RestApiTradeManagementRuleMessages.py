from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiTradeManagementRuleMessages(RestApiMessages):

    def find_all_trade_management_rule(self):
        self.clear_message_params()
        self.message_type = 'FindAllTradeManagementRule'
        return self

    def apply_rule(self, parameters):
        self.parameters = parameters
        return self

    def modify_trade_management_rule(self):
        self.message_type = 'ModifyTradeManagementRule'
        return self

    def enable_trade_management_rule(self):
        self.message_type = 'EnableTradeManagementRule'
        self.change_params({"alive": "false"})
        temp = self.get_parameters()["tradeManagementRuleCondition"]
        for index, instance in enumerate(temp):
            instance.update({"alive": "false"})
            instance["tradeManagementRuleResult"][0].update({"alive": "false"})
            temp[index].update(instance)
        return self

    def disable_trade_management_rule(self):
        self.message_type = 'DisableTradeManagementRule'
        self.change_params({"alive": "true"})
        temp = self.get_parameters()["tradeManagementRuleCondition"]
        for index, instance in enumerate(temp):
            instance.update({"alive": "true"})
            instance["tradeManagementRuleResult"][0].update({"alive": "true"})
            temp[index].update(instance)
        return self

    def change_result_by_index(self, result, condition_index=0):
        self.get_parameters()["tradeManagementRuleCondition"][condition_index]["tradeManagementRuleResult"].clear()
        self.get_parameters()["tradeManagementRuleCondition"][condition_index]["tradeManagementRuleResult"].append(
            result)
