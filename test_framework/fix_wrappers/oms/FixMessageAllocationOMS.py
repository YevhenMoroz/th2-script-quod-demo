from datetime import datetime

from custom import basic_custom_actions
from datetime import timezone
from test_framework.fix_wrappers.FixMessageAllocation import FixMessageAllocation
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageAllocationOMS(FixMessageAllocation):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

        self.base_parameters = {
            'TransactTime': datetime.utcnow().isoformat(),
            'TradeDate': datetime.now(timezone.utc).strftime('%Y%m%d'),
            'AllocTransType': '0',
            # 'AllocType': '2',
            'Shares': '100',
            'Side': '1',
            'AvgPx': '20'
        }

    def set_fix42_preliminary(self, new_order_single: FixMessageNewOrderSingle, alloc_acc):
        change_parameters = {
            'AllocID': basic_custom_actions.client_orderid(9),
            'NoAllocs': [
                {
                    'AllocShares': new_order_single.get_parameter("OrderQty"),
                    'AllocAccount': alloc_acc,
                }
            ],
            'Shares': new_order_single.get_parameter("OrderQty"),
            'Side': new_order_single.get_parameter("Side"),
            'AvgPx': new_order_single.get_parameter("Price"),
            "NoOrders": [
                {
                    'ClOrdID': new_order_single.get_parameter('ClOrdID'),
                }
            ],
            'Currency': new_order_single.get_parameter('Currency'),
            'NetMoney': str(
                float(new_order_single.get_parameter("OrderQty")) * float(new_order_single.get_parameter("Price"))),
            "Symbol": new_order_single.get_parameter("Symbol"),
            "SecurityID": new_order_single.get_parameter("SecurityID"),
            "IDSource": new_order_single.get_parameter("IDSource"),
            "SecurityExchange": new_order_single.get_parameter("SecurityExchange"),
            'GrossTradeAmt': str(
                float(new_order_single.get_parameter("OrderQty")) * float(new_order_single.get_parameter("Price"))),
        }
        self.change_parameters(self.base_parameters)
        self.change_parameters(change_parameters)
        return self
