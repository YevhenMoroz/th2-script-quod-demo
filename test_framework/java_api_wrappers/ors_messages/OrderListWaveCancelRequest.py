from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderListWaveCancelRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderListWaveCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_list_wave_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderListWaveCancelRequestBlock': {
                'OrderListWaveID': ord_list_wave_id
            }
        }
        super().change_parameters(base_parameters)
