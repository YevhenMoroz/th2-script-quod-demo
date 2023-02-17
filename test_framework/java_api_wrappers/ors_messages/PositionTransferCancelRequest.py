from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class PositionTransferCancelRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.PositionTransferCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, position_transfer_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'PositionTransferCancelRequestBlock': {
                "PositionTransferID": position_transfer_id
            }
        }
        super().change_parameters(base_parameters)
        return self
