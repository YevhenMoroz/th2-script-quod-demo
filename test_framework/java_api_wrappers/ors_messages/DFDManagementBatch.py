from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class DFDManagementBatch(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.DFDManagementBatch.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'DFDManagementBatchBlock': {
                "DFDOrderList": {"DFDOrderBlock":
                                     [{"OrdID": "*"}]
                                 },
                "SetDoneForDay": "Y"
            }
        }
        super().change_parameters(base_parameters)
