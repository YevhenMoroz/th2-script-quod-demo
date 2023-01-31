from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class HeldOrderAckReply(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.HeldOrderAckReply.value)
        super().change_parameters(parameters)

    def set_default(self, order_id) -> None:
        base_parameters = {
            'HeldOrderAckReplyBlock': {
                "RequestID": order_id,
                'HeldOrderAckType': 'Accept'
        }
        }
        super().change_parameters(base_parameters)
