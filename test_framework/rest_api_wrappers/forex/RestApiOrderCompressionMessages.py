from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiOrderCompressionMessages(RestApiMessages):

    def set_default_params(self, time):
        self.parameters = {
            "accountGroupID": "CLIENT_TEST_INT",
            "clientGroupID": "1",
            "enableCompression": "true",
            "executionDelay": "1",
            "orderCompressionName": "test",
            "orderCompressionTimeTable": [{"compressionTime": time}],
        }
        return self

    def create_order_compression(self):
        self.message_type = ResAPIMessageType.CreateOrderCompression.value
        return self

    def find_all_order_compression(self):
        self.clear_message_params()
        self.message_type = ResAPIMessageType.FindAllOrderCompression.value
        return self

    def delete_order_compression(self):
        self.message_type = ResAPIMessageType.DeleteOrderCompression.value
        return self
