from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class BookingCancelRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.BookingCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, allocation_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'BookingCancelRequestBlock': {
                'AllocInstructionID': allocation_id
            }
        }
        super().change_parameters(base_parameters)
        return self
