from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ManualMatchExecsToParentOrderRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.ManualMatchExecsToParentOrderRequest.value)
        self.change_parameters(parameters)

    def set_default_match_to_n(self, order_id, exec_ids: list, list_qty: list):
        manual_match_exec_param = []
        for exec_id in exec_ids:
            manual_match_exec_param.append({'ExecID': exec_id,
                                            'MatchingQty': list_qty[exec_ids.index(exec_id)]})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.CS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.CS',
            'ManualMatchExecsToParentOrderRequestBlock':
                {'ManualMatchExecList': {
                    'ManualMatchExecBlock':
                        manual_match_exec_param
                }, "ParentOrdID": order_id}}
        return self.change_parameters(base_parameters)