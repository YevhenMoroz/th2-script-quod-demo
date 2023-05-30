from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixPositionMassCancelRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.FixPositionMassCancelRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_params(self, party_id):
        request_params = {
            "SEND_SUBJECT": "QUOD.PKS.REQUEST",
            "REPLY_SUBJECT": "QUOD.PKS.REPLY",
            "PositionMassCancelRequestBlock": {
                "PartiesList": {
                    "PartiesBlock": [
                        {"PartyID": party_id,  # need set account like CLIENT1_1
                         "PartyIDSource": "Proprietary",
                         "PartyRole": "PositionAccount"}
                    ]
                },

            }
        }
        super().change_parameters(request_params)
        return self
