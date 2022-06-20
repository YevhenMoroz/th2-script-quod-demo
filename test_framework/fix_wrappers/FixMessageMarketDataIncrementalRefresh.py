from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs


class FixMessageMarketDataIncrementalRefresh(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.MarketDataIncrementalRefresh.value)
        super().change_parameters(parameters)

    def check_MDReqID(self, symbol: str, session_alias: str):
        list_MDRefID = Stubs.simulator.getAllMDRefID(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=session_alias)
        )).PairsMDRefID

        for field in list_MDRefID:
            if field.symbol == symbol:
                return field.MDRefID
        return None

    def check_MDReqIDFX(self, symbol: str, session_alias: str):
        md_ref_id = Stubs.simulator.getMDRefIDForConnection314(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=session_alias)
        )).MDRefID
        return md_ref_id

    def update_MDReqID(self, symbol: str, session_alias: str, type=None):
        if type == 'FX':
            md_req_id = self.check_MDReqIDFX(symbol, session_alias)
        else:
            md_req_id = self.check_MDReqID(symbol, session_alias)
        if md_req_id is None:
            raise Exception(f'No MDReqID at TH2 simulator for symbol {symbol} at {session_alias}')
        self.change_parameter("MDReqID", md_req_id)
        return self