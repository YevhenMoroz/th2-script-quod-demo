from datetime import datetime

from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.Instrument import Instrument


class FixMessageNewOrderSingle(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type="D")
        super().change_parameters(parameters)


