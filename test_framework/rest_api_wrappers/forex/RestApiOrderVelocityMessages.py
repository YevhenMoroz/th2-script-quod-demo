from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiOrderVelocityMessages(RestApiMessages):

    def find_all_limits(self):
        """
        Find all OrderVelocityLimit`s
        """
        self.clear_message_params()
        self.message_type = ResAPIMessageType.FindAllOrderVelocity.value
        return self

    def set_default_params(self):
        """
        Set default params for OrderVelocityLimit
        """
        self.parameters = {
            "instrSymbol": "EUR/USD",
            "side": "B",
            "accountGroupID": "CLIENT1",
            "movingTimeWindow": 30,
            "allOrders": "false",
            "autoResetRule": "true",
            "orderVelocityLimitID": random_qty(1, 7, 7),
            "maxCumOrdQty": 1000000,
            "orderVelocityLimitName": "Test_limit",
            "alive": "true"
        }
        return self

    def create_limit(self):
        """
        Create New OrderVelocityLimit
        """
        if "orderVelocityLimitID" in self.parameters.keys():
            self.remove_parameter("orderVelocityLimitID")
        self.message_type = ResAPIMessageType.CreateOrderVelocity.value
        return self

    def modify_limit(self):
        """
        Modify created OrderVelocityLimit
        """
        self.message_type = ResAPIMessageType.ModifyOrderVelocity.value
        return self

    def delete_limit(self):
        """
        Delete created OrderVelocityLimit
        """
        self.message_type = ResAPIMessageType.DeleteOrderVelocity.value
        return self
