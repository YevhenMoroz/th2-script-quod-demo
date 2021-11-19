from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import MessageType
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageOrderCancelRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.OrderCancelReplaceRequest.value)
        super().change_parameters(parameters)
