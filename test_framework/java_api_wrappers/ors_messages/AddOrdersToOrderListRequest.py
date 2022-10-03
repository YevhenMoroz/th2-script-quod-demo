
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class AddOrdersToOrderListRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.AddOrdersToOrderListRequest.value)
        super().change_parameters(parameters)

    def set_default(self, order_id, basket_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "AddOrdersToOrderListRequestBlock":
                    {"OrdIDList":
                        {"OrdIDBlock":
                            [{"OrdID": order_id}]
                         },
                     "OrderListID": basket_id}
                 }
        super().change_parameters(base_parameters)
