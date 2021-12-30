from datetime import datetime
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.forex import FixMessageQuoteRequestFX, FixMessageQuote


class FixMessageNewOrderMultiLeg(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.NewOrderMultiLeg.value)
        super().change_parameters(parameters)

    def set_default_prev_quoted_swap(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuote,
                                     price: str = None, side: str = None):
        quote_price = None
        if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
            if quote.get_parameter("Side") == "1":
                quote_price = quote.get_parameter("OfferPx")
            else:
                quote_price = quote.get_parameter("BidPx")

        base_parameters = {
            "ClOrdID": bca.client_orderid(9),
            "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
            "HandlInst": "1",
            "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
            quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
            "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"],
            "TimeInForce": "3",
            "OrdType": "D",
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": quote_price if quote_price is not None else price,
            "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
            "NoLegs": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
            # "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            # "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self
