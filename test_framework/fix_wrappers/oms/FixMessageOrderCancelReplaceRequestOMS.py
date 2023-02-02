from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest


class FixMessageOrderCancelReplaceRequestOMS(FixMessageOrderCancelReplaceRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

        self.base_parameters = {
            "Account": data_set.get_client_by_name("client_1"),
            "Side": "1",
            'OrderQtyData': {'OrderQty': '100'},
            "OrdType": "2",
            "HandlInst": "3",
            "ClOrdID": "*",
            "OrigClOrdID": "*",
            "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
            "TransactTime": datetime.utcnow().isoformat(),
        }

    def set_default(self, new_order_single: FixMessageNewOrderSingle, qty=None, price=None):
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
        if qty:
            change_parameters['OrderQtyData'] = {'OrderQty': qty}
        if price:
            change_parameters['Price'] = price
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_ord_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
