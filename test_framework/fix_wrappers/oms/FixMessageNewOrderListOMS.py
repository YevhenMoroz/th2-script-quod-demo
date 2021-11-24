from datetime import datetime, timedelta
from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList
from test_framework.fix_wrappers.DataSet import Instrument


class FixMessageNewOrderListOMS(FixMessageNewOrderList):

    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)


    base_parameters = {
        'BidType': "1",
        'TotNoOrders': '2',
        'ListID': basic_custom_actions.client_orderid(10),
        'ListOrdGrp': {'NoOrders': [{
            "Account": "CLIENT_FIX_CARE",
            "HandlInst": "3",
            "Side": "1",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': "CLIENT_FIX_CARE_SA1", 'AllocQty': "100"}]},
            "Instrument": Instrument.FR0010436584.value,
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": "EUR"
        }, {
            "Account": "CLIENT_FIX_CARE",
            "HandlInst": "3",
            "Side": "2",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "2",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': "CLIENT_FIX_CARE_SA1", 'AllocQty': "100"}]},
            "Instrument": Instrument.FR0010436584.value,
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": "EUR"
        }
        ]}
    }

    def set_default_order_list(self):
        self.change_parameters(self.base_parameters)
        return self
