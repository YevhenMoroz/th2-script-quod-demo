from datetime import datetime
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType


class FixOrderModificationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.FixOrderModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet, order_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'OrderModificationRequestBlock': {
                'ClOrdID': order_id,
                'OrigClOrdID': order_id,
                'OrdType': OrderType.limit.value,
                'Price': "20",
                'TimeInForce': 'DAY',
                'OrdQty': "100",
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'SettlCurrency': data_set.get_currency_by_name('currency_1'),
                'ClientAccountGroupID': data_set.get_client_by_name("client_1"),
            }
        }
        super().change_parameters(base_parameters)
        return self
