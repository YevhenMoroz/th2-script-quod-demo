from datetime import datetime

from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportOMS(FixMessageExecutionReport):

    def set_default_DMA(self):
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": DataSet.FR0010436584,
            "ExecType": "0",
            "OrdStatus": "0",
        }
        super().change_parameters(base_parameters)