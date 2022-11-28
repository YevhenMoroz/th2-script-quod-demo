from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuoteCancelFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.QuoteCancel.value)
        super().change_parameters(parameters)

    def set_params_for_cancel(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            QuoteCancelType="5"
        )
        super().change_parameters(temp)
        return self

    def set_params_for_receive(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            QuoteID="*",
            QuoteCancelType="5",
            NoQuoteEntries=[{
                "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]
            }]
        )
        super().change_parameters(temp)
        return self

    def set_params_for_receive_synergy(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            QuoteID="*",
            QuoteCancelType="5",
            VenueType=quote_request.get_parameter("VenueType"),
        )
        super().change_parameters(temp)
        return self
