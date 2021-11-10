from datetime import datetime
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.DataSet import Instrument


class FixMessageExecutionReportAlgoFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, new_order_single: FixMessageNewOrderSingle = None, ):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)


    def update_fix_message(self, parameters: dict) -> None:
        super().update_fix_message(parameters)
        temp = dict()
        temp["QuodFlatParameters"] = parameters["QuodFlatParameters"]
        temp["TargetStrategy"] = parameters["TargetStrategy"]
        super().change_parameters(temp)


