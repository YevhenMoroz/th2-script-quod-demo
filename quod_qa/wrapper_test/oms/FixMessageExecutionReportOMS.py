from datetime import datetime

from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportOMS(FixMessageExecutionReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        "HandlInst": "0",
        "Side": "1",
        "OrderQtyData": {'OrderQty': '100'},
        "TimeInForce": "0",
        "OrdType": "2",
        "TransactTime": datetime.utcnow().isoformat(),
        "OrderCapacity": "A",
        "Price": "20",
        "Currency": "EUR",
        "Instrument": DataSet.Instrument.FR0004186856.value,
    }

    def set_default_new(self):
        self.change_parameters(self.base_parameters)
        change_parameters = {
            'ExecID': '*',
            'ExpireDate': '*',
            'LastQty': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'AvgPx': '*',
            'Parties': '*',
            'SettlDate': '*',
            'HandlInst': '*',
            'LeavesQty': '*',
            'CumQty': '*',
            'LastPx': '*',
            'QtyType': '*',
            "ExecType": "0",
            "OrdStatus": "0",
        }
        self.change_parameters(change_parameters)
        return self

    def set_default_replaced(self):
        self.change_parameters(self.base_parameters)
        change_parameters = {
            'ExecID': '*',
            'LastQty': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'AvgPx': '*',
            'Parties': '*',
            'HandlInst': '*',
            'LeavesQty': '*',
            'CumQty': '*',
            'LastPx': '*',
            'QtyType': '*',
            "ExecType": "5",
            "OrdStatus": "0",
        }
        self.change_parameters(change_parameters)
        return self

    def set_default_cancel(self):
        self.change_parameters(self.base_parameters)
        change_parameters = {
            'ExecID': '*',
            'LastQty': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'AvgPx': '*',
            'Parties': '*',
            'HandlInst': '*',
            'LeavesQty': '*',
            'CumQty': '*',
            'LastPx': '*',
            'QtyType': '*',
            "ExecType": "4",
            "OrdStatus": "4",
        }
        self.change_parameters(change_parameters)
        return self

    def set_default_filled(self):
        self.change_parameters(self.base_parameters)
        change_parameters = {
            'ExecID': '*',
            'LastQty': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'AvgPx': '*',
            'Parties': '*',
            'HandlInst': '*',
            'LeavesQty': '*',
            'CumQty': '*',
            'LastPx': '*',
            'QtyType': '*',
            "ExecType": "F",
            "OrdStatus": "2",
            'SettlDate': '*',
            'ReplyReceivedTime': '*',
            'LastExecutionPolicy': '*',
            'TimeInForce': '*',
            'TradeDate': '*',
            'TradeReportingIndicator': '*',
            'OrdType': '1',
            'SecondaryOrderID': '*',
            'LastMkt': '*',
            'Text': '*',
            'SecondaryExecID': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*'

        }
        self.change_parameters(change_parameters)
        return self
