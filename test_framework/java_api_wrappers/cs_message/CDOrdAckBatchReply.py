from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDOrdAckBatchReply(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDOrdAckBatchReply.value)
        super().change_parameters(parameters)
