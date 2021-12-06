from datetime import datetime

from test_framework.fix_wrappers.FixMessageMarketDataRequest import FixMessageMarketDataRequest
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

class FixMessageMarketDataRequestFX(FixMessageMarketDataRequest):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_md_req_parameters(self) -> FixMessageMarketDataRequest:
        md_req_parameters = {
            'SenderSubID': 'CLIEN1',
            'MDReqID': bca.client_orderid(10),
            'MarketDepth': '0',
            'MDUpdateType': '0',
            'SubscriptionRequestType': '1',
            'BookType': '0',
            'NoMDEntryTypes': [
                {'MDEntryType': '0'},
                {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': {
                        'Symbol': 'EUR/USD',
                        'SecurityType': 'FXSPOT',
                        'Product': '4',
                    },
                    'SettlType': '0',
                }
            ]
        }
        super().change_parameters(md_req_parameters)
        return self


