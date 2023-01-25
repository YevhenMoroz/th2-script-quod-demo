from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDOrdAssign(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDOrdAssign.value)
        self.change_parameters(parameters)

    def set_default(self, ord_id, recipient_desk, recipient_user: str = None, recipient_role_id: str = None):
        assign_block = {}
        if not recipient_user and not recipient_role_id:
            assign_block.update({"OrdID": ord_id, "RecipientDeskID": recipient_desk})
        else:
            assign_block.update(
                {"OrdID": ord_id, "RecipientDeskID": recipient_desk, 'RecipientRoleID': recipient_role_id,
                 'RecipientUserID': recipient_user})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'CDOrdAssignBlock': assign_block
        }
        return self.change_parameters(base_parameters)
