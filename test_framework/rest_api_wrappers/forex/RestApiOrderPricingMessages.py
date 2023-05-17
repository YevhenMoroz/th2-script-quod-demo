from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiOrderPricingMessages(RestApiMessages):

    def set_default_params(self):
        self.parameters = {
            "accountGroupID": "CLIENT_TEST_INT",
            "clientGroupID": "1",
            "orderPricingName": "test",
            "pricingAgreement": "BEN",
            "rateMethodology": "MID",
            "rateSourceClientTierID": "4",
        }
        return self

    def create_order_pricing(self):
        self.message_type = ResAPIMessageType.CreateOrderPricing.value
        return self

    def find_all_order_pricing(self):
        self.clear_message_params()
        self.message_type = ResAPIMessageType.FindAllOrderPricing.value
        return self

    def delete_order_pricing(self):
        self.message_type = ResAPIMessageType.DeleteOrderPricing.value
        return self
