from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDOrdAssign(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDOrdAssign.value)
        self.change_parameters(parameters)

    def set_default(self, ord_id, recipient_desk):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'CDOrdAssignBlock':
                {
                    "OrdID": ord_id,
                    "RecipientDeskID": recipient_desk
                }
        }
        return self.change_parameters(base_parameters)