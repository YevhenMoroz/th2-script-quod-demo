from datetime import datetime, timedelta

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from stubs import Stubs
from test_framework.java_api_wrappers.ors_messages.TradeEntryRequest import TradeEntryRequest


class TradeEntryRequestOMS(TradeEntryRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        'SEND_SUBJECT': 'QUOD.ORS.FE',
        'TradeEntryRequestBlock': {
            'OrdID': "*",
            'ExecPrice': "10.000000000",
            'ExecQty': "100.000000000",
            'TradeEntryTransType': 'NEW',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'LastMkt': 'XPAR',
            'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'SettlDate': (tm(datetime.utcnow().isoformat()) + timedelta(days=2)).date().strftime(
                '%Y-%m-%dT%H:%M:%S')
        }
    }

    def set_default_trade(self, ord_id, exec_price="10", exec_qty="100"):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdID": ord_id, "ExecPrice": exec_price, 'ExecQty': exec_qty})
        return self
