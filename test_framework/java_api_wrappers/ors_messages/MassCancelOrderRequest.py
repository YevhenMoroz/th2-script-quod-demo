from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderMassCancelRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderMassCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, order_ids: list, cancel_child="N") -> None:
        list_of_orders_dict = []
        for item in order_ids:
            list_of_orders_dict.append({'OrdID': item})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderMassCancelRequestBlock': {
                'OrderList': {'OrderBlock': list_of_orders_dict},
                'CancelChildren': cancel_child
            }
        }
        super().change_parameters(base_parameters)
        return self

