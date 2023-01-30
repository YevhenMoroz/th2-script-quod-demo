from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


def set_list_of_execution(exec_ids):
    list_exec_ids = []
    for exec_id in exec_ids:
        list_exec_ids.append({'ExecID': exec_id})
    return list_exec_ids


class TradeEntryBatchRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.TradeEntryBatchRequest.value)
        super().change_parameters(parameters)
        self.list_of_orders_and_executions = []

    def set_orders_and_exec_id(self, order_id, exec_ids, exec_price, exec_qty):
        list_of_exec_ids = set_list_of_execution(exec_ids)
        self.list_of_orders_and_executions.append({
            'ExecToDiscloseList': {'ExecToDiscloseBlock': list_of_exec_ids},
            'OrdID': order_id,
            'ExecPrice': exec_price,
            'ExecQty': exec_qty,
            'TradeEntryTransType': 'CAL'
        })

    def set_default(self) -> None:
        base_parameters = {
            'Order_TradeEntryBatchRequest': {
                'TradeEntryRequestList': {
                    'TradeEntryRequestBlock': self.list_of_orders_and_executions
                }
            }
        }
        super().change_parameters(base_parameters)
