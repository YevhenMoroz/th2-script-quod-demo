from datetime import datetime

from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

class FixMessageMarketDataSnapshotFullRefreshBuyFX(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            "MDReqID": 'EUR/USD:SPO:REG:HSBC',
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': ('FXSPOT')
            },
            'NoMDEntries': [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18066,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18146,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self


