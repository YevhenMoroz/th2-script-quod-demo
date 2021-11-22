from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageExecutionReport(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(message_type=MessageType.ExecutionReport.value)
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> FixMessage:
        temp = dict(
            ExecID="*",
            OrderID="*",
            ClOrdID=parameters["ClOrdID"],
            Currency=parameters["Currency"],
            Instrument=parameters["Instrument"],
            OrderQty=parameters["OrderQty"],
            OrdType=parameters["OrdType"],
            Price=parameters["Price"],
            Side=parameters["Side"],
            TimeInForce=parameters["TimeInForce"],
            TransactTime="*",
        )
        super().change_parameters(temp)
        return self
