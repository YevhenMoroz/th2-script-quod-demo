from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDTransferAck(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDTransferAck.value)
        self.change_parameters(parameters)

    def set_default(self, cd_transfer_id, acceptor_desk_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'CDTransferAckBlock':
                {
                    "CDTransferID": cd_transfer_id,
                    "CDOrdResponse": 'A',
                    "AcceptorDeskID": acceptor_desk_id
                }
        }
        return self.change_parameters(base_parameters)
