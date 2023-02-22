from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ManualMatchExecToParentOrdersRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.ManualMatchExecToParentOrdersRequest.value)
        self.change_parameters(parameters)

    def set_default(self, order_id, match_qty, exec_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'ManualMatchExecToParentOrdersRequestBlock':
                {'ManualMatchParentOrderList': {
                    'ManualMatchParentOrderBlock':
                        [
                            {'ParentOrdID': order_id,
                             'MatchingQty': match_qty}
                        ]
                },
                    "ExecID": exec_id}
        }
        return self.change_parameters(base_parameters)
