from datetime import datetime
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.DataSet import Instrument


class FixMessageExecutionReportAlgo(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, new_order_single: FixMessageNewOrderSingle = None, ):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def set_default_TWAP(self) -> None:
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
            "Instrument": Instrument.FR0010436584,
            "ExecType": "0",
            "OrdStatus": "0",
        }
        super().change_parameters(base_parameters)

    def update_fix_message(self, parameters: dict) -> None:
        super().update_fix_message(parameters)
        temp = dict()
        temp["QuodFlatParameters"] = parameters["QuodFlatParameters"]
        temp["TargetStrategy"] = parameters["TargetStrategy"]
        super().change_parameters(temp)


