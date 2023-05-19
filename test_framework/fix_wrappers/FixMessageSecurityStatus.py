from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs


class FixMessageSecurityStatusRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.SecurityStatus.value)
        super().change_parameters(parameters)


    def check_SecurityStatusReqID(self, symbol: str, session_alias: str):
        list_SecurityStatusReqID = Stubs.simulator.getSecurityStatusReqIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=session_alias)
        )).PairsMDRefID

        for field in list_SecurityStatusReqID:
            if field.symbol == symbol:
                return field.MDRefID
        return None


    def update_SecurityStatusReqID(self, symbol: str, session_alias: str):
        security_status_req_id = self.check_SecurityStatusReqID(symbol, session_alias)
        if security_status_req_id is None:
            raise Exception(f'No SecurityStatusReqID at TH2 simulator for symbol {symbol} at {session_alias}')
        self.change_parameter("SecurityStatusReqID", security_status_req_id)
        return self