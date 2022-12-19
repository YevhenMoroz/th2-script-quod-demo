from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ForceAllocInstructionStatusBatchRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.ForceAllocInstructionStatusBatchRequest.value)
        super().change_parameters(parameters)

    def set_default(self, list_of_allocations) -> None:
        list_for_approve = []
        for alloc_id in list_of_allocations:
            list_for_approve.append({'AllocInstructionID': alloc_id,
                                     'AcknowledgeBlock': 'Y'})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "ForceAllocInstructionStatusBatchRequestBlock": {
                'ForceAllocInstructionStatusRequestList': {'ForceAllocInstructionStatusRequestBlock':
                                                               list_for_approve}
            }}
        super().change_parameters(base_parameters)
