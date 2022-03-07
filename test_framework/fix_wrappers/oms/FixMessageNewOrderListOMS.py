from datetime import datetime, timedelta

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList


class FixMessageNewOrderListOMS(FixMessageNewOrderList):

    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set=data_set

        self.base_parameters = {
            'BidType': "1",
            'TotNoOrders': '2',
            'ListID': basic_custom_actions.client_orderid(10),
            'ListOrdGrp': {'NoOrders': [{
                "Account": data_set.get_client_by_name("client_co_1"),
                "HandlInst": "3",
                "Side": "1",
                'OrderQtyData': {'OrderQty': "100"},
                "TimeInForce": "0",
                "OrdType": "2",
                'ListSeqNo': "1",
                'ClOrdID': basic_custom_actions.client_orderid(9),
                'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_co_1_acc_1"),
                                              'AllocQty': "100"}]},
                "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
                'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
                "TransactTime": datetime.utcnow().isoformat(),
                "Price": "20",
                "Currency": data_set.get_currency_by_name("currency_1")
            }, {
                "Account": data_set.get_client_by_name("client_co_1"),
                "HandlInst": "3",
                "Side": "2",
                'OrderQtyData': {'OrderQty': "100"},
                "TimeInForce": "0",
                "OrdType": "2",
                'ListSeqNo': "2",
                'ClOrdID': basic_custom_actions.client_orderid(9),
                'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_co_1_acc_1"),
                                              'AllocQty': "100"}]},
                "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
                'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
                "TransactTime": datetime.utcnow().isoformat(),
                "Price": "20",
                "Currency": data_set.get_currency_by_name("currency_1")
            }
            ]}
        }

    def set_default_order_list(self):
        self.change_parameters(self.base_parameters)
        return self

    def add_simple_order_to_list(self):
        parameters = self.base_parameters['ListOrdGrp']['NoOrders'].append(self.base_parameters['ListOrdGrp']['NoOrders'][0])
        self.change_parameters(parameters)
        return self


