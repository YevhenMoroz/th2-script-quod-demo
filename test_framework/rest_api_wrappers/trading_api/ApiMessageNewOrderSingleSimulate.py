from datetime import datetime

from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd


class ApiMessageNewOrderSingleSimulate(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.NewOrderSingleSimulate.value,
                         response_type_http=TradingRestApiMessageType.NewOrderSingleSimulateReply.value,
                         data_set=data_set)
        super().change_parameters(parameters)
        self.default_instrument_noss = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        self.default_currency_noss = self.data_set.get_currency_by_name('currency_1')
        self.default_settl_currency_noss = self.data_set.get_settl_currency_by_name('settl_currency_1')
        self.default_client_noss = self.data_set.get_client_by_name('client_4')
        self.default_account_noss = self.data_set.get_account_by_name('account_4')
        self.default_cash_account_noss = self.data_set.get_cash_account_by_name('cash_account_1')

    def set_default_request(self):
        base_parameters = {'ClOrdID': bca.client_orderid(9),
                           'Side': 'Buy',
                           'OrdType': 'Limit',
                           'Price': 1,
                           'Currency': self.default_currency_noss,
                           'SettlCurrency': self.default_settl_currency_noss,
                           'TimeInForce': 'Day',
                           'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                               '%Y-%m-%dT%H:%M:%S'),
                           'ClientAccountGroupID': self.default_client_noss,
                           'ClientCashAccountID': self.default_cash_account_noss,
                           'PreTradeAllocations': [
                               {
                                   'AllocClientAccountID': self.default_account_noss,
                                   'AllocQty': 1
                               }
                           ],
                           'OrdQty': 1,
                           'Instrument': {
                               'InstrSymbol': self.default_instrument_noss['InstrSymbol'],
                               'SecurityID': self.default_instrument_noss['SecurityID'],
                               'SecurityIDSource': self.default_instrument_noss['SecurityIDSource'],
                               'InstrType': self.default_instrument_noss['InstrType'],
                               'SecurityExchange': self.default_instrument_noss['SecurityExchange']
                           }
                           }
        super().change_parameters(base_parameters)
