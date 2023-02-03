
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ListCancelRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.ListCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, basket_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "ListCancelRequestBlock":
                    {"OrderListID": basket_id}
                 }
        super().change_parameters(base_parameters)
