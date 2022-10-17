from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderBagWaveModificationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagWaveModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_bag_wave_id, qty_to_release, ord_type, tif):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderBagWaveModificationRequestBlock': {
                'OrderBagWaveID': ord_bag_wave_id,
                "QtyToRelease": qty_to_release,
                "OrdType": ord_type,
                "TimeInForce": tif,
            }
        }
        super().change_parameters(base_parameters)
