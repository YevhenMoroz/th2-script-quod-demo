from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.DataSet import MessageType


class FixMessageMarketDataRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.MarketDataRequest.value)
        super().change_parameters(parameters)
