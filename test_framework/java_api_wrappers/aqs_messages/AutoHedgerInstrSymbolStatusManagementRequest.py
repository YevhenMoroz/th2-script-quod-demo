from test_framework.data_sets.message_types import AQSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class AutoHedgerInstrSymbolStatusManagementRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=AQSMessageType.AutoHedgerInstrSymbolStatus.value)
        self.change_parameters(parameters)

    def set_default(self, hedger_id, instr, send_orders):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.AQS.FE",
            "REPLY_SUBJECT": "QUOD.FE.AQS",
            "AutoHedgerInstrSymbolStatusManagementRequestBlock": {
                "AutoHedgerID": hedger_id,
                "InstrSymbol": instr,
                "SendHedgeOrders": send_orders,
            }
        }
        return self.change_parameters(base_parameters)
