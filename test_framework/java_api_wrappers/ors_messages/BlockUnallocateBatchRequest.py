from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class BlockUnallocateBatchRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.BlockUnallocateBatchRequest.value)
        super().change_parameters(parameters)

    def set_default(self, list_of_alloc_id) -> None:
        list_of_allocations = []
        for alloc_id in list_of_alloc_id:
            list_of_allocations.append({'AllocInstructionID': alloc_id})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "BlockUnallocateBatchRequestBlock": {
                'AllocationInstructionCancelRequestList': {
                    'AllocationInstructionCancelRequestBlock':
                        list_of_allocations
                }
            }
        }
        super().change_parameters(base_parameters)
