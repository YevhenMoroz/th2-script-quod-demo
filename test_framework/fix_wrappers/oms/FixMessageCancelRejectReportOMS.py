from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport


class FixMessageOrderCancelRejectReportOMS(FixMessageOrderCancelRejectReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    def set_default_cancel_replace_request(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "OrderID": new_order_single.get_parameter("ClOrdID"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "OrigClOrdID": new_order_single.get_parameter("ClOrdID"),
            "OrderStatus": '0',
            "CxlRejResponseTo": '2'
        }
        self.change_parameters(change_parameters)
        return self

    def set_default__cancel_request(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "OrderID": new_order_single.get_parameter("ClOrdID"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "OrigClOrdID": new_order_single.get_parameter("ClOrdID"),
            "OrderStatus": '0',
            "CxlRejResponseTo": '1'
        }
        self.change_parameters(change_parameters)
        return self
