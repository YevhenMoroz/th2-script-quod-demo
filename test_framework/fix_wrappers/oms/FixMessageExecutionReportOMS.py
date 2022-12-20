from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportOMS(FixMessageExecutionReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

        self.base_parameters = {
            "Account": data_set.get_client_by_name("client_1"),
            "HandlInst": "0",
            "Side": "1",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": data_set.get_currency_by_name("currency_1"),
            "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
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
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Side": new_order_single.get_parameter("Side"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": "*",
            "SettlDate": "*"
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_new_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],
            "ExpireDate": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ExpireDate"],
            "SettlDate": "*"
        }
        if new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"] == "2":
            change_parameters.update({"Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"]})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_filled(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "F",
            "OrdStatus": "2",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Side": new_order_single.get_parameter("Side"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
            "SettlDate": "*",
            "SecondaryOrderID": "*",
            "LastExecutionPolicy": "*",
            "TradeDate": "*",
            "TradeReportingIndicator": "*",
            "SecondaryExecID": "*",
            "ExDestination": "*",
            "GrossTradeAmt": "*",
            "SettlCurrency": "*",
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_filled_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "ExecType": "F",
            "OrdStatus": "2",
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],
            "SettlDate": "*",
            "SecondaryOrderID": "*",
            "LastExecutionPolicy": "*",
            "TradeDate": "*",
            "TradeReportingIndicator": "*",
            "SecondaryExecID": "*",
            "ExDestination": "*",
            "GrossTradeAmt": "*",
            "ReplyReceivedTime": "*",
            "ExpireDate": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ExpireDate"],
        }
        if new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"] == "2":
            change_parameters.update({"Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"]})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_replaced(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "5",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_replaced_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "ExecType": "5",
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],

        }
        if new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"] == "2":
            change_parameters.update({"Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"]})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_canceled(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "4",
            "OrdStatus": "4",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_rejected(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "8",
            "OrdStatus": "8",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            'OrigClOrdID': new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_canceled_list(self, new_order_list: FixMessageNewOrderList, ord_number: int = 0):
        change_parameters = {
            "ExecType": "4",
            "OrdStatus": "4",
            "Account": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Account"],
            "OrderQtyData": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrderQtyData"],
            "HandlInst": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["HandlInst"],
            "ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            'OrigClOrdID': new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["ClOrdID"],
            "Side": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Side"],
            "OrdType": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"],
            "TimeInForce": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["TimeInForce"],
            "Instrument": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Instrument"],

        }
        if new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["OrdType"] == "2":
            change_parameters.update({"Price": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][ord_number]["Price"]})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_trade_cancel(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "H",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "Side": new_order_single.get_parameter("Side"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
            "ExecRefID": '*',
            "SettlCurrency": '*',
            "SettlDate": '*',
            "LastExecutionPolicy": '*',
            'TradeDate': '*',
            "TradeReportingIndicator": '*',
            "SecondaryOrderID": '*',
            "SecondaryExecID": '*',
            "ExDestination": '*',
            "GrossTradeAmt": '*'
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self


    def set_default_calculated(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            "ExecType": "B",
            "OrdStatus": "B",
            "Account": new_order_single.get_parameter("Account"),
            "OrderQtyData": new_order_single.get_parameter("OrderQtyData"),
            "ClOrdID": new_order_single.get_parameter("ClOrdID"),
            "HandlInst": new_order_single.get_parameter("HandlInst"),
            "Side": new_order_single.get_parameter("Side"),
            "OrdType": new_order_single.get_parameter("OrdType"),
            "TimeInForce": new_order_single.get_parameter("TimeInForce"),
            "Instrument": new_order_single.get_parameter("Instrument"),
            "AvgPx": "*",
            "SettlDate": "*",
            "TradeReportingIndicator": "*",
            "ExDestination": "*",
            "GrossTradeAmt": "*"
        }
        if new_order_single.get_parameter("OrdType") == "2":
            change_parameters.update({"Price": new_order_single.get_parameter("Price")})
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
