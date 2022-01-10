from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType


class FixMessageMarketDataRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.MarketDataRequest.value)
        super().change_parameters(parameters)
