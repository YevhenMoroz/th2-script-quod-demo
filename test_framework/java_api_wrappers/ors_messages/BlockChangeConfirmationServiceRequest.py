from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class BlockChangeConfirmationServiceRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.BlockChangeConfirmationServiceRequest.value)
        super().change_parameters(parameters)

    def set_default(self, alloc_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "BlockChangeConfirmationServiceRequestBlock": {
                'AllocInstructionID': alloc_id,
                'ConfirmationService': "MAN"}
        }
        super().change_parameters(base_parameters)
