from datetime import datetime, timedelta

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageNewOrderList import FixMessageNewOrderList


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
            'OrderQtyData': {'OrderQty': "900"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': "CLIENT_FIX_CARE_SA1", 'AllocQty': "900"}]},
            "Instrument": Instrument.FR0004186856.value,
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": "EUR"
        }, {
            "Account": "CLIENT_FIX_CARE",
            "HandlInst": "3",
            "Side": "2",
            'OrderQtyData': {'OrderQty': "900"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "2",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': "CLIENT_FIX_CARE_SA1", 'AllocQty': "900"}]},
            "Instrument": Instrument.FR0004186856.value,
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
