from datetime import datetime

from custom.tenor_settlement_date import wk1
from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd


class FixMessageMarketDataSnapshotFullRefreshBuyFX(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            "MDReqID": "EUR/USD:SPO:REG:HSBC",
            "LastUpdateTime": datetime.utcnow().strftime('%Y%m%d-%H:%M:%S'),
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
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18151,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1813,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18165,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.181,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18186,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                }
            ],

        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_fwd(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            "MDReqID": "EUR/USD:FXF:WK1:HSBC",
            "Instrument": {
                "Symbol": "EUR/USD",
                "SecurityType": "FXFWD"
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1815,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18151,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1813,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18165,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.181,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18186,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": wk1(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_md_for_deposit_and_loan_spot(self):
        base_parameters = {
            "MDReqID": "USD:SPO:REG:D3",
            "Instrument": {
                "Symbol": "USD",
                "SecurityType": "FXSPOT"
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 0.1,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 0.1,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S"),
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_md_for_deposit_and_loan_fwd(self):
        base_parameters = {
            "MDReqID": "USD:FXF:WK1:D3",
            "Instrument": {
                "Symbol": "USD",
                "SecurityType": "FXFWD"
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 0.04,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 0.05,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000001",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 0.03,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 0.06,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000002",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 0.02,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 0.07,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 1,
                    "MDEntryForwardPoints": "0.0000003",
                    "SettlDate": wk1(),
                    "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self
