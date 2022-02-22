from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ModifyBagOrderRequest(JavaApiMessage):

    def __init__(self,parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_id1, ord_id2, order_bag_id, price: str, bag_name: str) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'OrderBagModificationRequestBlock': {
                'OrderBagOrderList': {
                    'OrderBagOrderBlock': [
                        {'OrdID': ord_id1},
                        {'OrdID': ord_id2},
                    ]
                },
                'OrderBagID': order_bag_id,
                'Price': price,
                'OrderBagName': bag_name
            }
        }
        super().change_parameters(base_parameters)
