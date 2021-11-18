from datetime import datetime

from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportOMS(FixMessageExecutionReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        "HandlInst": "0",
        "Side": "1",
        "OrderQtyData": {'OrderQty': '100'},
        "TimeInForce": "0",
        "OrdType": "2",
        "TransactTime": datetime.utcnow().isoformat(),
        "OrderCapacity": "A",
        "Price": "20",
        "Currency": "EUR",
        "Instrument": DataSet.Instrument.FR0004186856.value,
        "ExecType": "0",
        "OrdStatus": "0",
    }

    def set_default(self):
        self.change_parameters(self.base_parameters)
        return self