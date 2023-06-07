from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs
from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh


class FixMessageMarketDataSnapshotFullRefreshAlgo(FixMessageMarketDataSnapshotFullRefresh):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def check_MDReqID(self, symbol: str, session_alias: str):
        list_MDRefID = Stubs.simulator_algo.getAllMDRefID(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=session_alias)
        )).PairsMDRefID

        for field in list_MDRefID:
            if field.symbol == symbol:
                return field.MDRefID
        return None

    def update_MDReqID(self, symbol: str, session_alias: str, type=None):

        md_req_id = self.check_MDReqID(symbol, session_alias)
        if md_req_id is None:
            raise Exception(f'No MDReqID at TH2 simulator for symbol {symbol} at {session_alias}')
        self.change_parameter("MDReqID", md_req_id)
        return self


    def set_market_data(self, best_bid = 30, best_ask = 40) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            'MDReqID': "2754",
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': best_bid,
                    'MDEntrySize': '1000000',
                    'MDEntryPositionNo': '1',
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': best_ask,
                    'MDEntrySize': '1000000',
                    'MDEntryPositionNo': '1',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_empty(self) -> FixMessageMarketDataSnapshotFullRefresh:
        base_parameters = {
            'MDReqID': "2754",
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '0',
                    'MDEntrySize': '0',
                    'MDEntryPositionNo': '1',
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '0',
                    'MDEntrySize': '0',
                    'MDEntryPositionNo': '1',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self