from datetime import datetime

from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.DataSet import Instrument, MessageType


class FixMessageMarketDataIncrementalRefresh(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.MarketDataIncrementalRefresh.value)
        super().change_parameters(parameters)