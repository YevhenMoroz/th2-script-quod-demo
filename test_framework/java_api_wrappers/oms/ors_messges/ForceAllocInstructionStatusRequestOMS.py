from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusRequest import \
    ForceAllocInstructionStatusRequest


class ForceAllocInstructionStatusRequestOMS(ForceAllocInstructionStatusRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "ForceAllocInstructionStatusRequestBlock": {"AllocInstructionID": "*", "AcknowledgeBlock": "Y"}}

    def set_default_approve(self, alloc_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('ForceAllocInstructionStatusRequestBlock',
                                        {"AllocInstructionID": alloc_id})
        return self
