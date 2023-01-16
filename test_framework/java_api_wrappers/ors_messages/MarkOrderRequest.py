from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class MarkOrderRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.MarkOrderRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_id, reviewed="Y") -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'MarkOrderRequestBlock': {'MarkOrderList': {'MarkOrderBlock': [{'OrdID': ord_id}]},
                                      'MarkAsReviewed': reviewed}
        }
        super().change_parameters(base_parameters)
