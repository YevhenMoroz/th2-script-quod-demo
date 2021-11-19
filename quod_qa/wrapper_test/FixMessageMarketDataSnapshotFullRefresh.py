from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from quod_qa.wrapper_test.DataSet import MessageType
from quod_qa.wrapper_test.FixMessage import FixMessage
from stubs import Stubs


class FixMessageMarketDataSnapshotFullRefresh(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.MarketDataSnapshotFullRefresh.value)
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

    def update_MDReqID(self, symbol: str, session_alias: str):
        md_req_id = self.check_MDReqID(symbol, session_alias)
        if md_req_id is None:
            raise Exception(f'No MDReqID at TH2 simulator for symbol {symbol} at {session_alias}')
        self.change_parameter("MDReqID", md_req_id)
        return self
