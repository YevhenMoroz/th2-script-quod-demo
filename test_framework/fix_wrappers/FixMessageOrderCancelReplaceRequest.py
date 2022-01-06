from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage


class FixMessageOrderCancelReplaceRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.OrderCancelReplaceRequest.value)
        super().change_parameters(parameters)
