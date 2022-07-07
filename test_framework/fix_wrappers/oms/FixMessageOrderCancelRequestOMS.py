from datetime import datetime

from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageOrderCancelRequestOMS(FixMessageOrderCancelRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    def set_default(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "OrigClOrdID": new_order_single.get_parameter("ClOrdID"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "Account": new_order_single.get_parameter("Account"),
            "TransactTime": datetime.utcnow().isoformat()
        }
        self.change_parameters(change_parameters)
        return self

    def set_default_ord_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "TransactTime": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TransactTime"],
        }
        self.change_parameters(change_parameters)
        return self
