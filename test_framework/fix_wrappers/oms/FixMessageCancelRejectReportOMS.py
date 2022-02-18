from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport


class FixMessageOrderCancelRejectReportOMS(FixMessageOrderCancelRejectReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    def set_default(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "Account": new_order_single.get_parameter("Account"),
            "OrdStatus": '0',
            "Text": "*",
            "OrderID": "*",
            "TransactTime": "*",
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "OrigClOrdID": new_order_single.get_parameter("ClOrdID")
        }
        self.change_parameters(change_parameters)
        return self
