from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDOrdAckBatchRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDOrdAckBatchRequest.value)
        self.change_parameters(parameters)

    def set_default(self, order_id, cd_ord_notif_id, desk_id, set_reject=False):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'CDOrdAckBatchRequestBlock':
                {'CDOrderAckList': {
                    'CDOrderAckBlock':
                        [
                            {'OrdID': order_id,
                             'CDOrdNotifID': cd_ord_notif_id}
                        ]
                },
                    'CDOrdResponse': 'A',
                    'CDOrdAckType': 'N',
                    'AcceptorDeskID': desk_id}
        }
        if set_reject:
            base_parameters["CDOrdAckBatchRequestBlock"]["CDOrdResponse"] = "R"
        return self.change_parameters(base_parameters)
