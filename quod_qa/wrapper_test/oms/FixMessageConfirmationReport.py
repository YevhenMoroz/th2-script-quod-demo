from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageConfirmationReport(FixMessage):

    def __init__(self, fix_message: FixMessage = None, parameters: dict = None):
        super().__init__(message_type='Confirmation')
        if fix_message is not None:
            self.update_fix_message(fix_message.get_parameters())
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
