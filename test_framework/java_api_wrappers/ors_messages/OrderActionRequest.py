from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderActionRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagCancelReply.value)
        super().change_parameters(parameters)

    def set_default(self, order_ids: []) -> None:
        orders_list = []
        for order in order_ids:
            orders_list.append({'OrdID': order})
        base_parameters = {
            'OrderBagCancelReplyBlock': {
                'OrderAction': "DSE",
                'DiscloseExec': "M",
                'OrderActionRequestBlock': {'OrderActionList': {'OrderActionBlock': orders_list}}
            }
        }
        super().change_parameters(base_parameters)
