from test_framework.fix_wrappers.FixMessageAllocationInstructionReport import FixMessageAllocationInstructionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageAllocationInstructionReportOMS(FixMessageAllocationInstructionReport):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        'Account': "MOClient",
        'AllocType': '5',
        'BookingType': '0',
        'AllocTransType': '0',
        'Quantity': '100',
        'Side': '1',
        'AvgPx': '20'
    }

    def set_default_ready_to_book(self, new_order_single: FixMessageNewOrderSingle):
        change_parameters = {
            'Account': new_order_single.get_parameter('Account'),
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'Quantity': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'TransactTime': '*',
            'ReportedPx': '*',
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
            'Instrument': '*',
            'TradeDate': '*',
            'GrossTradeAmt': '*',
            'LastMkt': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_preliminary(self, new_order_single: FixMessageNewOrderSingle):
        no_allocs = new_order_single.get_parameter('PreAllocGrp')['NoAllocs']
        for no_alloc in no_allocs:
            no_alloc.update(AllocNetPrice=new_order_single.get_parameter("Price"))
            no_alloc.update(AllocPrice=new_order_single.get_parameter("Price"))

        change_parameters = {
            'Account': new_order_single.get_parameter('Account'),
            'AllocType': '2',
            'NoAllocs': no_allocs,
            'BookingType': '0',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'Quantity': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'TransactTime': '*',
            'AllocTransType': '0',
            'ReportedPx': '*',
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
            'Instrument': '*',
            'TradeDate': '*',
            'GrossTradeAmt': '*',
            'LastMkt': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self

    def set_default_calculated (self, new_order_single: FixMessageNewOrderSingle):
        no_allocs = new_order_single.get_parameter('PreAllocGrp')['NoAllocs']
        for no_alloc in no_allocs:
            no_alloc.update(AllocNetPrice=new_order_single.get_parameter("Price"))
            no_alloc.update(AllocPrice=new_order_single.get_parameter("Price"))

        change_parameters = {
            'Account': new_order_single.get_parameter('Account'),
            'AllocType': '1',
            'NoAllocs': no_allocs,
            'BookingType': '0',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'Quantity': new_order_single.get_parameter("OrderQtyData")['OrderQty'],
            'LastMkt': new_order_single.get_parameter('ExDestination'),
            'TransactTime': '*',
            'AllocTransType': '0',
            'ReportedPx': '*',
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
            'Instrument': '*',
            'TradeDate': '*',
            'GrossTradeAmt': '*'
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
