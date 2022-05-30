from datetime import datetime

from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from pandas import Timestamp as tm


class ApiMessageNewOrderSingle(TradingRestApiMessage):

    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__(request_type_http=TradingRestApiMessageType.NewOrderSingle.value,
                         response_type_http=TradingRestApiMessageType.NewOrderSingleReply.value,
                         message_type_web_socket=TradingRestApiMessageType.OrderUpdate.value,
                         data_set=data_set)
        super().change_parameters(parameters)
        self.tested_instrument_nos = self.data_set.get_trading_api_instrument_by_name("instrument_2")

    def set_default_request(self):
        base_parameters = {'ClOrdID': bca.client_orderid(9),
                           'Side': 'Buy',
                           'OrdType': 'Limit',
                           'Price': 1,
                           'Currency': self.data_set.get_currency_by_name('currency_1'),
                           'SettlCurrency': "INR",
                           'TimeInForce': 'Day',
                           'TransactTime': tm(datetime.utcnow().isoformat()),
                           'ClientAccountGroupID': self.data_set.get_client_by_name('client_4'),
                           'PreTradeAllocations': [
                               {
                                   'AllocClientAccountID': self.data_set.get_account_by_name('account_4'),
                                   'AllocQty': 1
                               }
                           ],
                           'OrdQty': 1,
                           'Instrument': {
                               'InstrSymbol': self.tested_instrument_nos['InstrSymbol'],
                               'SecurityID': self.tested_instrument_nos['SecurityID'],
                               'SecurityIDSource': self.tested_instrument_nos['SecurityIDSource'],
                               'InstrType': self.tested_instrument_nos['InstrType'],
                               'SecurityExchange': self.tested_instrument_nos['SecurityExchange']
                           }
                           }
        super().change_parameters(base_parameters)
