from quod_qa.wrapper_test.FixMessageConfirmationReport import FixMessageConfirmationReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageConfirmationReportOMS(FixMessageConfirmationReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        'AllocQty': '100',
        'AllocAccount': 'MOClient_SA1',
        'ConfirmType': '2',
        'Side': '1',
        'AvgPx': '20',
        'QuodTradeQualifier':'AL',
        'Currency':'EUR',
        'NetMoney':'2000',
        'MatchStatus':'0',
        'ConfirmStatus': '1',
        'LastMkt': 'XPAR',
        'GrossTradeAmt':'2000',
    }

    def set_default_confirmation_new(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            'ConfirmTransType': "0",
            'AllocQty': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'AllocAccount': '*',
            'TransactTime': '*',
            'Side': new_order_single.get_parameter("Side"),
            'AvgPx': new_order_single.get_parameter("Price"),
            'QuodTradeQualifier': '*',
            'BookID': '*',
            'NoOrders': [{
                'ClOrdID': new_order_single.get_parameter('ClOrdID'),
                'OrderID': '*'
            }],
            'SettlDate': '*',
            'AllocID': '*',
            'Currency':new_order_single.get_parameter('Currency'),
            'NetMoney': '*',
            'TradeDate': '*',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'LastMkt':new_order_single.get_parameter('ExDestination'),
            'CpctyConfGrp': '*',
            'ReportedPx': new_order_single.get_parameter("Price"),
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_confirmation_replace(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            'ConfirmTransType': "1",
            'AllocQty': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'AllocAccount': '*',
            'TransactTime': '*',
            'Side': new_order_single.get_parameter("Side"),
            'AvgPx': new_order_single.get_parameter("Price"),
            'QuodTradeQualifier': '*',
            'BookID': '*',
            'NoOrders': [{
                'ClOrdID': new_order_single.get_parameter('ClOrdID'),
                'OrderID': '*'
            }],
            'SettlDate': '*',
            'AllocID': '*',
            'Currency': new_order_single.get_parameter('Currency'),
            'NetMoney': '*',
            'TradeDate': '*',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'LastMkt': new_order_single.get_parameter('ExDestination'),
            'CpctyConfGrp': '*',
            'ReportedPx': new_order_single.get_parameter("Price"),
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_confirmation_cancel(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            'ConfirmTransType': "2",
            'AllocQty': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'AllocAccount': '*',
            'TransactTime': '*',
            'Side': new_order_single.get_parameter("Side"),
            'AvgPx': new_order_single.get_parameter("Price"),
            'QuodTradeQualifier': '*',
            'BookID': '*',
            'NoOrders': [{
                'ClOrdID': new_order_single.get_parameter('ClOrdID'),
                'OrderID': '*'
            }],
            'SettlDate': '*',
            'AllocID': '*',
            'Currency': new_order_single.get_parameter('Currency'),
            'NetMoney': '*',
            'TradeDate': '*',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'LastMkt': new_order_single.get_parameter('ExDestination'),
            'CpctyConfGrp': '*',
            'ReportedPx': new_order_single.get_parameter("Price"),
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
