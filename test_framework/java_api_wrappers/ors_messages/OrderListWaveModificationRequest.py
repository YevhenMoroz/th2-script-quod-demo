from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.java_api_constants import QtyPercentageProfile


class OrderListWaveModificationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderListWaveModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, wave_id: str, ord_id_list: list, list_id: str, percent_qty="1",
                    profile=QtyPercentageProfile.RemainingQty.value):
        id_list = list()
        for ord_id in ord_id_list:
            id_list.append({'ParentOrdID': ord_id})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderListWaveModificationRequestBlock': {
                'ParentOrdrList': {'ParentOrdrBlock': id_list},
                'OrderListWaveID': wave_id,
                'OrderListID': list_id,
                'PercentQtyToRelease': percent_qty,
                'QtyPercentageProfile': profile

            }
        }
        super().change_parameters(base_parameters)
