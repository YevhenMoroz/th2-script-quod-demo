from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs
from test_framework.fix_wrappers.FixMessageMarketDataIncrementalRefresh import FixMessageMarketDataIncrementalRefresh
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

    def set_market_data_incr_refresh_ltq(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '2754',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_market_data_incr_refresh_iiv_pop(self) -> FixMessageMarketDataIncrementalRefresh:
        base_parameters = {
            'MDReqID': '2754',
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': 'Q',
                    'MDEntryPx': '40',
                    'MDEntrySize': '3000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '2',
                    'SecurityTradingStatus': '3',
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self


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