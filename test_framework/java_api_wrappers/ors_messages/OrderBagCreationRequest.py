from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderBagCreationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagCreationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, child_creation_policy, bag_name, ord_id_list: list):
        id_list = list()
        for ord_id in ord_id_list:
            id_list.append({'OrdID': ord_id})
        base_parameters = {

            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderBagCreationRequestBlock': {
                'OrderBagOrderList': {'OrderBagOrderBlock': id_list},
                "ChildCreationPolicy": child_creation_policy,
                "OrderBagName": bag_name,

            }
        }
        super().change_parameters(base_parameters)
