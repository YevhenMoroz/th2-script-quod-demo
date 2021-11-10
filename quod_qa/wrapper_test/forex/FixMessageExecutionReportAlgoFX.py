from datetime import datetime
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.DataSet import Instrument


class FixMessageExecutionReportAlgoFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, new_order_single: FixMessageNewOrderSingle = None):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_to_pending_new(self, new_order_single: FixMessageNewOrderSingle) -> None:
        initial = new_order_single.get_parameters()
        temp = dict(
            ExecType="A",
            OrdStatus="A",
            Text="Hello sim",
            LeavesQty=initial["OrderQty"],
            CumQty=initial["OrderQty"],
            Currency=initial["Currency"],
            AvgPx="0",
            LastQty="0",
        )
        super().change_parameters(temp)



