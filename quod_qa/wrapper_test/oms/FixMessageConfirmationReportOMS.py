from datetime import datetime

from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.oms.FixMessageConfirmationReport import FixMessageConfirmationReport


class FixMessageConfirmationReportOMS(FixMessageConfirmationReport):
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
        'SettlType': '0',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }

    def set_default_confirmation(self):
        self.change_parameters(self.base_parameters)
        change_parameters = {
            'ExecID': '*',
            'LastQty': '*',
            'OrderID': '*',
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
            'SecondaryOrderID': '*',
            'LastMkt': '*',
            'Text': '*',
            'SettlType': '0',
            'SecondaryExecID': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*'

        }
        self.change_parameters(change_parameters)
        return self
