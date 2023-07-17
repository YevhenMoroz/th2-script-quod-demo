from datetime import datetime, timezone

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.FixOrderModificationRequest import FixOrderModificationRequest


class FixOrderModificationRequestFX(FixOrderModificationRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'REPLY_SUBJECT': 'QUOD.FIX_REPLY.gtwquod8',
            'OrderModificationRequestBlock': {
                'ClOrdID': "*",
                'OrigClOrdID': "*",
                'OrdType': 'Market',
                'TimeInForce': 'DAY',
                'OrdQty': "1000000",
                'TransactTime': (tm(datetime.now(timezone.utc).isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'SettlCurrency': data_set.get_currency_by_name('currency_eur'),
                'ClientAccountGroupID': "ASPECT_CITI",
            },
        }

    def set_modify_order_limit(self, cl_ord_id, qty="1000000", price="1.18"):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrderModificationRequestBlock',
                                        {'ClOrdID': cl_ord_id, 'OrigClOrdID': cl_ord_id, "OrdType": 'Limit',
                                         "Price": price, "OrdQty": qty})
        return self

    def set_modify_order_market(self, cl_ord_id, qty="1000000"):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrderModificationRequestBlock',
                                        {'ClOrdID': cl_ord_id, 'OrigClOrdID': cl_ord_id, "OrdQty": qty})
        return self
