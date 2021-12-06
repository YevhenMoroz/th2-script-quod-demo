from datetime import datetime
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest


class FixMessageOrderCancelReplaceRequestOMS(FixMessageOrderCancelReplaceRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        "Side": "1",
        'OrderQtyData': {'OrderQty': '100'},
        "OrdType": "2",
        "HandlInst": "3",
        "ClOrdID": "*",
        "OrigClOrdID": "*",
        "Instrument": Instrument.FR0010436584.value,
        "TransactTime": datetime.utcnow().isoformat(),
    }

    def set_default(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "Price": new_order_single.get_parameter("Price"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "Instrument":  new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
