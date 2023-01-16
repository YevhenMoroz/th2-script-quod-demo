from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageConfirmationReport import FixMessageConfirmationReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageConfirmationReportOMS(FixMessageConfirmationReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

        self.base_parameters = {
            'AllocQty': '100',
            'AllocAccount': data_set.get_account_by_name("client_co_1_acc_1"),
            'ConfirmType': '2',
            'Side': '1',
            'AvgPx': '20',
            'QuodTradeQualifier': 'AL',
            'Currency': data_set.get_currency_by_name("currency_1"),
            'NetMoney': '2000',
            'MatchStatus': '0',
            'ConfirmStatus': '1',
            'GrossTradeAmt': '2000',
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
                'OrderID': '*',
                'OrderAvgPx': new_order_single.get_parameter("Price"),  # New?
            }],
            'SettlDate': '*',
            'AllocID': '*',
            'Currency': new_order_single.get_parameter('Currency'),
            'NetMoney': '*',
            'TradeDate': '*',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'CpctyConfGrp': '*',
            'ReportedPx': '*',
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*',

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
            'CpctyConfGrp': '*',
            'ReportedPx': '*',
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*',
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
            'CpctyConfGrp': '*',
            'ReportedPx':'*',
            'Instrument': '*',
            'GrossTradeAmt': '*',
            'ConfirmID': '*',
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
