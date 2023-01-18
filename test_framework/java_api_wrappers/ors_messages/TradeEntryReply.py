from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class TradeEntryReply(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.TradeEntryReply.value)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {}
        super().change_parameters(base_parameters)
