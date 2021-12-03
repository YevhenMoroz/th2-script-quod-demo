from datetime import datetime

from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportOMS(FixMessageExecutionReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        "HandlInst": "0",
        "Side": "1",
        'OrderQtyData': {'OrderQty': "100"},
        "TimeInForce": "0",
        "OrdType": "2",
        "OrderCapacity": "A",
        "Price": "20",
        "Currency": "EUR",
        "Instrument": DataSet.Instrument.FR0010436584.value,
        "ExecType": "0",
        "OrdStatus": "0",
        "OrderID": "*",
        "ExecID": "*",
        "LastQty": "*",
        "TransactTime": "*",
        "AvgPx": "*",
        "Parties": "*",
        "LeavesQty": "*",
        "CumQty": "*",
        "LastPx": "*",
        "QtyType": "*",

    }

    def set_default_new(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "Price":new_order_single.get_parameter("Price"),
            "ClOrdID":new_order_single.get_parameter("ClOrdID"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Side": new_order_single.get_parameter("Side"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
            "SettlDate": "*",
            "ReplyReceivedTime": "*",
            "SecondaryOrderID": "*",
            "Text": "*"

        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_new_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],
            "SettlDate": "*",
            "ReplyReceivedTime": "*",
            "SecondaryOrderID": "*",
            "Text": "*"

        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_filled(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "F",
            "OrdStatus": "2",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "Price": new_order_single.get_parameter("Price"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Side": new_order_single.get_parameter("Side"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
            "SettlDate": "*",
            "ReplyReceivedTime": "*",
            "SecondaryOrderID": "*",
            "Text": "*",
            "LastExecutionPolicy": "*",
            "TradeDate": "*",
            "TradeReportingIndicator": "*",
            "SecondaryExecID": "*",
            "ExDestination": "*",
            "GrossTradeAmt": "*",
            'MiscFeesGrp': "*",
            'CommissionData': '*',

        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_replaced(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "5",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "Price": new_order_single.get_parameter("Price"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_replaced_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "ExecType": "5",
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],

        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_canceled(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "4",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "Price": new_order_single.get_parameter("Price"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_canceled_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "ExecType": "4",
            "OrdStatus": "4",
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],

        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
