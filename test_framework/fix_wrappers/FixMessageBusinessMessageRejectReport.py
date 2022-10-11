from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage


class FixMessageBusinessMessageRejectReport(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.BusinessMessageReject.value)
        self.update_fix_message()
        super().change_parameters(parameters)

    def update_fix_message(self) -> None:
        temp = dict(
            RefSeqNum='*',
            Text='*',
            RefMsgType='G',
            BusinessRejectReason='5',
        )
        super().change_parameters(temp)