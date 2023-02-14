from datetime import datetime

from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageAllocation import FixMessageAllocation
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageAllocationOMS(FixMessageAllocation):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

        self.base_parameters = {
            # 'Account': "MOClient",
            # 'AllocType': '5',
            # 'BookingType': '0',
            'AllocTransType': '0',
            # 'Quantity': '100',
            'Side': '1',
            'AvgPx': '20'
        }

    def set_fix42_preliminary(self, new_order_single: FixMessageNewOrderSingle, no_allocs=None):
        if 'PreAllocGrp' in new_order_single.get_parameters():
            no_allocs = new_order_single.get_parameter('PreAllocGrp')['NoAllocs']
            for no_alloc in no_allocs:
                no_alloc.update(AllocNetPrice=new_order_single.get_parameter("Price"))
                no_alloc.update(AllocPrice=new_order_single.get_parameter("Price"))

        change_parameters = {
            # 'Account': new_order_single.get_parameter('Account'),
            'NoAllocs': "1",
            'Shares': new_order_single.get_parameter("OrderQty"),
            'TransactTime': datetime.utcnow().isoformat(),
            'AllocTransType': '0',
            'Side': new_order_single.get_parameter("Side"),
            'AvgPx': new_order_single.get_parameter("Price"),
            'AllocID': basic_custom_actions.client_orderid(9),
            'NoOrders': "1",
            'Currency': new_order_single.get_parameter('Currency'),
            'NetMoney': '2000',
            "Symbol": new_order_single.get_parameter("Symbol"),
            "SecurityID": new_order_single.get_parameter("SecurityID"),
            "IDSource": new_order_single.get_parameter("IDSource"),
            "SecurityExchange": new_order_single.get_parameter("SecurityExchange"),
            'TradeDate': datetime.utcnow().isoformat(),
            'GrossTradeAmt': '2000',
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self