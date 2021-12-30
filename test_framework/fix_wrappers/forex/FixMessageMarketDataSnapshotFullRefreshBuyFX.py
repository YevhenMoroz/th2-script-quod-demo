from datetime import datetime

from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd


class FixMessageMarketDataSnapshotFullRefreshBuyFX(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            "MDReqID": "EUR/USD:SPO:REG:HSBC",
            "Instrument": {
                "Symbol": "EUR/USD",
                "SecurityType": "FXSPOT"
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1815,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18151,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1813,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18165,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.181,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18186,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_fwd(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            "MDReqID": "EUR/USD:FXF:WK1:HSBC",
            "Instrument": {
                "Symbol": "EUR/USD",
                "SecurityType": "FXSPOT"
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1815,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18151,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1813,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18165,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.181,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18186,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self
