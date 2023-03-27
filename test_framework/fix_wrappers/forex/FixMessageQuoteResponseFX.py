from test_framework.data_sets.constants import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from custom import basic_custom_actions as bca


class FixMessageQuoteResponseFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.QuoteResponse.value)
        super().change_parameters(parameters)

    def set_params_for_quote_response(self, quote: FixMessageQuoteFX, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteRespID=bca.client_orderid(8),
            QuoteID=quote.get_parameter("QuoteID"),
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            QuoteRespType="8",
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            Product="4"),

        )
        super().change_parameters(temp)
        return self
