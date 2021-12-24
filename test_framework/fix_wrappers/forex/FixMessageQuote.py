from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuote(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.Quote.value)
        super().change_parameters(parameters)

    def set_params_for_quote(self, quote_request: FixMessageQuoteRequestFX):
        self.prepare_params_for_quote(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidPx": "*"})
            self.add_tag({"OfferSpotRate": "*"})
            self.add_tag({"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"OfferPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"Side": "1"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
            self.remove_parameter("OfferPx")
            self.remove_parameter("OfferSize")
            self.remove_parameter("OfferSpotRate")
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidPx": "*"})
        return self

    def prepare_params_for_quote(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteMsgID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            OfferPx="*",
            OfferSize=quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"],
            ValidUntilTime="*",
            OfferSpotRate="*",
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            Product="4"),
            SettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            SettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            Currency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            QuoteType=quote_request.get_parameter("NoRelatedSymbols")[0]["QuoteType"],
        )
        super().change_parameters(temp)
        return self
