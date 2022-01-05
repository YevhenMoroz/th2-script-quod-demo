from test_framework.java_api_wrappers.JavaApiDataSet import ORSMessages, QtyPercentageProfile
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderListWaveCreationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessages.OrderListWaveCreationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, list_id, ord_id1, ord_id2, percent_qty="1", profile=QtyPercentageProfile.RemainingQty.value):
        base_parameters = {

            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'OrderListWaveCreationRequestBlock': {
                'ParentOrdrList': {'ParentOrdrBlock': [{'ParentOrdID': ord_id1},
                                                       {'ParentOrdID': ord_id2}]},
                'OrderListID': list_id,
                'PercentQtyToRelease': percent_qty,
                'QtyPercentageProfile': profile

            }
        }
        super().change_parameters(base_parameters)
