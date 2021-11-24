from datetime import datetime

from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.DataSet import Instrument, MessageType


class FixMessageNewOrderSingle(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.NewOrderSingle.value)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "Instrument": Instrument.FR0010436584.value,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
        }
        super().change_parameters(base_parameters)
