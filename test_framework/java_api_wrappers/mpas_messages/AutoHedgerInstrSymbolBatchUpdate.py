from test_framework.data_sets.message_types import  MPASMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class AutoHedgerInstrSymbolBatchUpdate(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MPASMessageType.AutoHedgerInstrSymbolBatchUpdate.value)
        self.change_parameters(parameters)

    def set_default(self):
        base_parameters = {
            "AutoHedgerInstrSymbolBatchUpdateBlock": {
            }
        }
        return self.change_parameters(base_parameters)