from test_framework.java_api_wrappers.ors_messages.HeldOrderAckRequest import HeldOrderAckRequest


class HeldOrderAckRequestFX(HeldOrderAckRequest):

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)
        super().change_parameters(parameters)

    def set_default_ack(self, order_id):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.ORS.FE",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "HeldOrderAckBlock": {
                "RequestID": order_id,
                "RequestType": "NEW",
                "HeldOrderAckType": "A",
                "FreeNotes": "Ack by user"
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_rej(self, order_id):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.ORS.FE",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "HeldOrderAckBlock": {
                "RequestID": order_id,
                "RequestType": "NEW",
                "HeldOrderAckType": "R",
                "FreeNotes": "Rejected by user"
            }
        }
        super().change_parameters(base_parameters)
        return self
