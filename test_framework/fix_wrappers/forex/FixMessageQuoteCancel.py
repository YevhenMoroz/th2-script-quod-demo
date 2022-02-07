from test_framework.data_sets.constants import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuoteCancelFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.QuoteCancel.value)
        super().change_parameters(parameters)

    def set_params_for_cancel(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            QuoteID="*",
            QuoteCancelType="5"
        )
        super().change_parameters(temp)
        return self
