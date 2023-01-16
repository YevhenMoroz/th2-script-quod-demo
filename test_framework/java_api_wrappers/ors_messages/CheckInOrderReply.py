from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CheckInOrderReply(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.CheckInOrderReply.value)
        super().change_parameters(parameters)

    def set_default(self, order_id) -> None:
        base_parameters = {
            'CheckInOrderReplyBlock': {
                "OrdID": order_id
        }
        }
        super().change_parameters(base_parameters)
