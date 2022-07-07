from test_framework.fix_wrappers.FixMessageMarketDataIncrementalRefresh import FixMessageMarketDataIncrementalRefresh
from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from datetime import datetime


class FixMessageMarketDataIncrementalRefreshAlgo(FixMessageMarketDataIncrementalRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data_incr_refresh(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '2754',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3_000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

