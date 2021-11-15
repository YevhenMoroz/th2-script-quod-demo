from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh


class FixMessageMarketDataSnapshotFullRefreshAlgo(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_market_data(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            'MDReqID': "2754",
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '1000000',
                    'MDEntryPositionNo': '1',
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '1000000',
                    'MDEntryPositionNo': '1',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self
