from datetime import datetime

from test_framework.fix_wrappers.FixMessageListCancelRequest import FixMessageListCancelRequest
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageListCancelRequestOMS(FixMessageListCancelRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    def set_default_ord_list(self, list_id):
        change_parameters = {
            'ListID': list_id,
            "TransactTime": datetime.utcnow().isoformat(),
        }
        self.change_parameters(change_parameters)
        return self
