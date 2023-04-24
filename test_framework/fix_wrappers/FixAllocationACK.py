from datetime import timezone
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from pandas import Timestamp as tm
from datetime import datetime

class FixAllocationACK(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.AllocationACK.value)
        super().change_parameters(parameters)

    def set_default(self, alloc_id, alloc_status):
        base_parameters = {
            'AllocID': alloc_id,
            "AllocStatus": alloc_status,
            "TradeDate": tm(datetime.now(timezone.utc).isoformat()).date().strftime('%Y%m%d'),
        }
        super().change_parameters(base_parameters)
