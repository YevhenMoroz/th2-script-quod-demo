from datetime import datetime
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

    def set_default(self, data_set: BaseDataSet, order_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderModificationRequestBlock': {
                'OrdID': order_id,
                'OrdType': OrderType.limit.value,
                'Price': "20",
                'TimeInForce': 'DAY',
                'PositionEffect': 'O',
                'OrdQty': "100",
                'OrdCapacity': 'A',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': '1',
                'BookingType': 'REG',
                'SettlCurrency': data_set.get_currency_by_name('currency_1'),
                'CancelChildren': 'N',
                'ModifyChildren': 'N',
                'RouteID': data_set.get_route_id_by_name("route_1"),
                'ExecutionPolicy': 'C',
                'AccountGroupID': data_set.get_client_by_name("client_1"),
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_amend_counterparts(self, order_id, counterpart_list):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderModificationRequestBlock': {
                'OrdID': order_id,
                'CounterpartList': {'CounterpartBlock': counterpart_list}
            }
        }
        super().change_parameters(base_parameters)
        return self
