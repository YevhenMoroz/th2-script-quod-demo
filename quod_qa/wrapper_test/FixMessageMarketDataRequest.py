from datetime import datetime

from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.DataSet import Instrument, MessageType


class FixMessageMarketDataRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.MarketDataRequest.value)
        super().change_parameters(parameters)
