from datetime import datetime, timedelta

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType


class OrderModificationRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderModificationRequest.value)
        super().change_parameters(parameters)

    def set_param(self, data_set: BaseDataSet,order_id, price, new_qty, client) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderModificationRequestBlock': {
                'OrdID': order_id,
                'OrdType': OrderType.limit.value,
                'Price': price,
                'TimeInForce': 'DAY',
                'PositionEffect': 'O',
                'OrdQty': new_qty,
                'OrdCapacity': 'A',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': '1',
                'BookingType': 'REG',
                'SettlCurrency': data_set.get_currency_by_name('currency_1'),
                'CancelChildren': 'N',
                'ModifyChildren': 'N',
                'RouteID': 1,
                'ExecutionPolicy': 'C',
                'AccountGroupID': client,
                'WashBookAccountID': data_set.get_washbook_account_by_name('washbook_account_3')
            }
        }
        super().change_parameters(base_parameters)
