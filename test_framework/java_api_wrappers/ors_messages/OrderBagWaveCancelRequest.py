from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderBagWaveCancelRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagWaveCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_bag_wave_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderBagWaveCancelRequestBlock': {
                "OrderBagWaveID": ord_bag_wave_id
            }
        }
        super().change_parameters(base_parameters)
