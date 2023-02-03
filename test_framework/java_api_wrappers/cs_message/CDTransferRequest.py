from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDTransferRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDTransferRequest.value)
        self.change_parameters(parameters)

    def set_default_send_on_user(self, order_id, recipient_user_id, recipient_role_id, recipient_desk_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'CDTransferRequestBlock':
                {'OrderTransferList': {
                    'OrderTransferBlock':
                        [
                            {'OrdID': order_id}
                        ]
                },
                    'RecipientUserID': recipient_user_id,
                    'RecipientRoleID': recipient_role_id,
                    'RecipientDeskID': recipient_desk_id}
        }
        return self.change_parameters(base_parameters)
