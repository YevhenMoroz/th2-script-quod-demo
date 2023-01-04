from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class HeldOrderAckRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.HeldOrderAckRequest.value)
        super().change_parameters(parameters)

    def set_default(self, order_id, client) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'HeldOrderAckBlock': {
                'RequestID': order_id,
                'RequestType': 'NEW',
                'HeldOrderAckType': 'A',
                'AccountGroupID': client
            }
        }
        super().change_parameters(base_parameters)
        return self