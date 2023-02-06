from test_framework.data_sets.message_types import AQSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class FrontendQueryReply(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=AQSMessageType.FrontendQueryReply.value)
        self.change_parameters(parameters)