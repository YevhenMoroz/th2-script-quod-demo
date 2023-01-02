from datetime import datetime, timedelta

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.TradeEntryRequest import TradeEntryRequest


class TradeEntryOMS(TradeEntryRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'TradeEntryRequestBlock': {
                'OrdID': "*",
                'ExecPrice': "10.000000000",
                'ExecQty': "100.000000000",
                'TradeEntryTransType': 'NEW',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'LastMkt': self.data_set.get_mic_by_name("mic_1"),
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'SettlDate': (tm(datetime.utcnow().isoformat()) + timedelta(days=2)).date().strftime(
                    '%Y-%m-%dT%H:%M:%S')
            }
        }

    def set_default_trade(self, ord_id, exec_price="10", exec_qty="100"):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('TradeEntryRequestBlock',
                                        {"OrdID": ord_id, "ExecPrice": exec_price, 'ExecQty': exec_qty})
        return self

    def set_default_cancel_execution(self, order_id, exec_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('TradeEntryRequestBlock',
                                        {"OrdID": order_id, "ExecPrice": '0', 'ExecQty': '0',
                                         'TradeEntryTransType': 'CAN', 'ExecRefID': exec_id})
