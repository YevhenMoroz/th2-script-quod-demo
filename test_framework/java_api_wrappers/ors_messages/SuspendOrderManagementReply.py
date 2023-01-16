from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class SuspendOrderManagementReply(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.SuspendOrderManagementRequest.value)
        super().change_parameters(parameters)

    def set_default(self, order_id, suspend_order="Y", cancel_children="N") -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "SuspendOrderManagementReplyBlock":
                {"OrdID": order_id,
                 "SuspendOrder": suspend_order,
                 "CancelChildren": cancel_children
                 }
        }
        super().change_parameters(base_parameters)
