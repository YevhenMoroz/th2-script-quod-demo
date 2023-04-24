from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class MatchCptyMOBlocksRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.MatchCptyMOBlocksRequest.value)
        super().change_parameters(parameters)

    def set_default(self, fix_alloc_id, alloc_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "MatchCptyMOBlocksRequestBlock": {"CptyAllocInstructionID": fix_alloc_id, "MOAllocInstructionID": alloc_id}}
        super().change_parameters(base_parameters)
