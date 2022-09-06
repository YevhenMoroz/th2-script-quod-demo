from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderAcknowledge(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.Order_CDOrdAckBatchRequest.value)
        self.change_parameters(parameters)

    def set_default(self, order_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'CDOrdAckBatchRequestBlock':
                {'CDOrderAckList': {
                    'CDOrderAckBlock':
                        [
                            {'OrdID': order_id}
                        ]
                },
                    'CDOrdResponse': 'A',
                    'CDOrdAckType': 'N',
                    'AcceptorDeskID': '10'}
        }
        self.change_parameters(base_parameters)
