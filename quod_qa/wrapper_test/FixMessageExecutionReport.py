from datetime import datetime

from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageExecutionReport(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(message_type="ExecutionReport")
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> FixMessage:
        temp = dict(
            Account=parameters["Account"],
            ClOrdID=parameters["ClOrdID"],
            Currency=parameters["Currency"],
            HandlInst=parameters["HandlInst"],
            Instrument=parameters["Instrument"],
            OrderQty=parameters["OrderQty"],
            OrdType=parameters["OrdType"],
            Price=parameters["Price"],
            Side=parameters["Side"],
            TimeInForce=parameters["TimeInForce"],
            ExecType="0",
            OrdStatus="0",
            TransactTime=datetime.utcnow().isoformat(),
        )
        super().change_parameters(temp)
        return self

    def change_from_new_to_pendingnew(self) -> FixMessage:
        super().change_parameters(
            dict(
                ExecType="A",
                OrdStatus="A",
            )
        )
        return self