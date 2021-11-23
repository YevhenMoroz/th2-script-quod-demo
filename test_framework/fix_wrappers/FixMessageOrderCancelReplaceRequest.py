from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage


class FixMessageOrderCancelReplaceRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.OrderCancelReplaceRequest.value)
        super().change_parameters(parameters)
