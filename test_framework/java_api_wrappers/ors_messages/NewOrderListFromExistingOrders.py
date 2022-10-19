import random
import string

from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class NewOrderListFromExistingOrders(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.NewOrderList.value)
        super().change_parameters(parameters)

    '''
    list_of_orders is list which include dicts with follow structure:
    {OrdID:"CO1221019100752056001"},{OrdID:"CO1221019100752056001"}
    '''

    def set_default(self, list_of_orders: list, basket_name: str = None) -> None:
        if basket_name is None:
            basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'NewOrderListBlock': {'OrdIDList': {'OrdIDBlock': list_of_orders},
                                  'OrderListName': basket_name
                                  }
        }
        super().change_parameters(base_parameters)
