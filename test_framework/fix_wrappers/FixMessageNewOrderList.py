from datetime import datetime
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixMessage import FixMessage


class FixMessageNewOrderList(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type="NewOrderList")
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            'BidType': "1",
            'TotNoOrders': '2',
            'ListOrdGrp': {'NoOrders': [{
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
            }, {
                "Account": "CLIENT1",
                "HandlInst": "0",
                "Side": "2",
                "OrderQty": "1000",
                "TimeInForce": "0",
                "OrdType": "2",
                "Instrument": Instrument.test.value,
                "TransactTime": datetime.utcnow().isoformat(),
                "OrderCapacity": "A",
                "Price": "20",
                "Currency": "EUR",
                "ExDestination": "XPAR",
            }
            ]}
        }
        super().change_parameters(base_parameters)
