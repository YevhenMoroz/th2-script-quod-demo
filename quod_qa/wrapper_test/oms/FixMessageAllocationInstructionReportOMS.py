from datetime import datetime

from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.oms.FixMessageAllocationInstructionReport import FixMessageAllocationInstructionReport


class FixMessageAllocationInstructionReportOMS(FixMessageAllocationInstructionReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
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
        'AllocType': '2',
        'Text': '*',
        'SettlType': '0',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }

    def set_default_allocation(self):
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
            'AllocType': '2',
            'Text': '*',
            'SettlType': '0',
            'SecondaryExecID': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*'

        }
