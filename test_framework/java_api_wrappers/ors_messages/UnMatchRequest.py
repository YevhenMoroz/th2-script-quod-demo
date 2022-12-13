from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class UnMatchRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.UnMatchRequest.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet, exec_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'UnMatchRequestBlock': {'UnMatchingList': {'UnMatchingBlock': [
                {'VirtualExecID': exec_id,
                 'UnMatchingQty': '100',
                 'SourceAccountID': data_set.get_washbook_account_by_name('washbook_account_3'),
                 'PositionType': 'N'}
            ]
            }
            }
        }
        super().change_parameters(base_parameters)

    def set_default_unmatch_and_transfer(self, possition_account: str):
        self.update_fields_in_component('UnMatchRequestBlock', {'DestinationAccountID': possition_account})
