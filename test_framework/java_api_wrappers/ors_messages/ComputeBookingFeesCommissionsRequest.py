from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ComputeBookingFeesCommissionsRequest(JavaApiMessage):
    def __init__(self, data_set, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.Order_ComputeBookingFeesCommissionsRequest.value,
                         data_set=data_set)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'ComputeBookingFeesCommissionsRequestBlock': {
            }
        }
        super().change_parameters(base_parameters)
