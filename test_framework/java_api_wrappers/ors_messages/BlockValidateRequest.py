from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class BlockValidateRequest(JavaApiMessage):

    def __init__(self,data_set, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.BlockValidateRequest.value)
        super().change_parameters(parameters)
        self.data_set = data_set

    def set_default(self, alloc_id,alloc_inst_acc_id, client, account, price="20", qty="100"):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'BlockValidateRequestBlock': {
                "AllocAccountList":
                    {"AllocAccountBlock": [{"AllocInstructionAccountID": alloc_inst_acc_id, "AllocAccountID": account,
                                            "AllocPrice": price, "AllocQty": qty}]},
                "AllocInstructionID": alloc_id,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                "AccountGroupID": client}
        }
        super().change_parameters(base_parameters)
