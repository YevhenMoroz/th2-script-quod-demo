from datetime import datetime

from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.DataSet import Instrument


class FixMessageMarketDataRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type="MarketDataRequest")
        super().change_parameters(parameters)