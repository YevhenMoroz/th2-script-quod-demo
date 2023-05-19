from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from stubs import Stubs


class FixMessageSecurityStatusRequest(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.SecurityStatusRequest.value)
        super().change_parameters(parameters)