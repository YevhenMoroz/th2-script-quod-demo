from datetime import datetime

from custom.tenor_settlement_date import wk1
from test_framework.fix_wrappers.FixMessageMarketDataIncrementalRefresh import FixMessageMarketDataIncrementalRefresh
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd


class FixMessageMarketDataIncrementalRefreshBuyFX(FixMessageMarketDataIncrementalRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            "MDReqID": "EUR/USD:SPO:REG:HSBC",

            "NoMDEntriesIR": [
                {
                    "MDUpdateAction": "0",
                    "MDEntryType": "0",
                    "MDEntryID": bca.client_orderid(12),
                    "MDEntryPx": 1.18111,
                    "MDEntrySize": 2000000,
                    "QuoteEntryID": bca.client_orderid(12),
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDUpdateAction": "0",
                    "MDEntryType": "1",
                    "MDEntryID": bca.client_orderid(12),
                    "MDEntryPx": 1.18222,
                    "MDEntrySize": 2000000,
                    "QuoteEntryID": bca.client_orderid(12),
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                }
            ],

        }
        super().change_parameters(base_parameters)
        return self

