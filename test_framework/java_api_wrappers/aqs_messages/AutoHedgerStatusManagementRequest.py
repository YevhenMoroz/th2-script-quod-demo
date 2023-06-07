from test_framework.data_sets.message_types import AQSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class AutoHedgerStatusManagementRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=AQSMessageType.AutoHedgerStatusManagementRequest.value)
        self.change_parameters(parameters)

    def send_hedge_orders_true(self):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.AQS.FE",
            "REPLY_SUBJECT": "QUOD.FE.AQS",
            "AutoHedgerStatusManagementRequestBlock": {
                "AutoHedgerStatusID": "1",
                "SendHedgeOrders": "Y",
            }
        }
        return self.change_parameters(base_parameters)

    def send_hedge_orders_false(self):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.AQS.FE",
            "REPLY_SUBJECT": "QUOD.FE.AQS",
            "AutoHedgerStatusManagementRequestBlock": {
                "AutoHedgerStatusID": "1",
                "SendHedgeOrders": "N",
            }
        }
        return self.change_parameters(base_parameters)
