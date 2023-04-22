from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle
from test_framework.data_sets.base_data_set import BaseDataSet


class FixMessageExecutionReport(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None,
                 data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.ExecutionReport.value, data_set=data_set)
        # self.__data_set = data_set
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
