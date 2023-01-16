from test_framework.data_sets.message_types import FIXMessageType, ORSMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX


class FixMessageQuoteCancelFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.QuoteCancel.value)
        super().change_parameters(parameters)

    def set_params_for_cancel(self, quote_request, quote):
        fix_request = FIXMessageType.QuoteRequest.value
        java_api_request = ORSMessageType.QuoteRequest.value
        if quote_request.get_message_type() is fix_request:
            temp = dict(
                QuoteReqID=quote_request.get_parameter("QuoteReqID"),
                QuoteID=quote.get_parameter("QuoteID"),
                QuoteCancelType="5"
            )
            super().change_parameters(temp)
            return self
        elif quote_request.get_message_type() is java_api_request:
            temp = dict(
                QuoteReqID=quote_request.get_parameter("QuoteRequestBlock")["ClientQuoteReqID"],
                QuoteID=quote.get_parameter("QuoteID"),
                QuoteCancelType="5"
            )
            super().change_parameters(temp)
            return self
        else:
            err = str(type(quote_request)).rsplit(".")[-1].replace("\'>", "")
            raise AttributeError(f"\"FixMessageQuoteCancelFX\" doesn\'t support \"{err}\" object")


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
