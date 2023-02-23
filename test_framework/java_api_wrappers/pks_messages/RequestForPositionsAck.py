from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class RequestForPositionsAck(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=PKSMessageType.RequestForPositionsAck.value)
        super().change_parameters(parameters)