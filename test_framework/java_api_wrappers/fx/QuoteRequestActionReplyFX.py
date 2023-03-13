from test_framework.java_api_wrappers.ors_messages.QuoteRequestActionReply import QuoteRequestActionReply


class QuoteRequestActionReplyFX(QuoteRequestActionReply):

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)

    def set_default(self) -> None:
        base_parameters = {
            "QuoteRequestActionReplyBlock": {}}
        super().change_parameters(base_parameters)
