import copy
from datetime import datetime
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex import FixMessageQuoteRequestSynergyFX, FixMessageQuoteSynergyFX


class FixMessageNewOrderMultiLegSynergyFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.NewOrderMultiLeg.value)
        super().change_parameters(parameters)

    def set_default_prev_quoted_multileg(self, quote_request: FixMessageQuoteRequestSynergyFX,
                                         quote: FixMessageQuoteSynergyFX,
                                         price: str = None, side: str = None):
        quote_price = None
        # if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
        #     if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
        #         quote_price = quote.get_parameter("OfferSwapPoints")
        #     else:
        #         quote_price = quote.get_parameter("BidSwapPoints")

        base_parameters = {
            "ClOrdID": bca.client_orderid(9),
            "SecondaryClOrdID": bca.client_orderid(9),
            "NoPartyIDs": quote_request.get_parameter("NoRelatedSym")[0]["NoPartyIDs"],
            "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSym")[0] else
            quote_request.get_parameter("NoRelatedSym")[0]["NoLegs"][0]["LegSide"],
            "OrderQty": quote_request.get_parameter("NoRelatedSym")[0]["NoLegs"][0]["LegQty"],
            "OrdType": "D",
            "TransactTime": datetime.utcnow().isoformat(),
            "Currency": quote_request.get_parameter("NoRelatedSym")[0]["Currency"],
            "Instrument": quote_request.get_parameter("NoRelatedSym")[0]["Instrument"],
            "NoLegs": quote_request.get_parameter("NoRelatedSym")[0]["NoLegs"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        base_parameters["NoLegs"][0].update({"LegPrice": price, "LegID": quote.get_parameter("NoLegs")[0]["LegRefID"]})
        base_parameters["NoLegs"][1].update({"LegPrice": price, "LegID": quote.get_parameter("NoLegs")[1]["LegRefID"]})
        base_parameters["NoPartyIDs"].append(copy.deepcopy(quote_request.get_parameter("NoRelatedSym")[0]["NoPartyIDs"][0]))
        base_parameters["NoPartyIDs"][1].update({"PartyRole": "3"})
        super().change_parameters(base_parameters)
        return self
    # TODO add other messages
    # def set_default_prev_quoted_swap_ccy2(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
    #                                       price: str = None, side: str = None):
    #     quote_price = None
    #     if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
    #         if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
    #             quote_price = quote.get_parameter("BidSwapPoints")
    #         else:
    #             quote_price = quote.get_parameter("OfferSwapPoints")
    #
    #     base_parameters = {
    #         "ClOrdID": bca.client_orderid(9),
    #         "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
    #         "HandlInst": "1",
    #         "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
    #         quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
    #         "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
    #         "TimeInForce": "3",
    #         "OrdType": "D",
    #         "TransactTime": datetime.utcnow().isoformat(),
    #         "Price": quote_price if quote_price is not None else price,
    #         "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
    #         "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
    #         "NoLegs": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
    #         "QuoteID": quote.get_parameter("QuoteID")
    #     }
    #
    #     super().change_parameters(base_parameters)
    #     return self
    #
    # def set_default_prev_quoted_swap_ndf(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
    #                                      price: str = None, side: str = None):
    #     quote_price = None
    #     if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
    #         if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
    #             quote_price = quote.get_parameter("OfferSwapPoints")
    #         else:
    #             quote_price = quote.get_parameter("BidSwapPoints")
    #
    #     base_parameters = {
    #         "ClOrdID": bca.client_orderid(9),
    #         "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
    #         "HandlInst": "1",
    #         "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
    #         quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
    #         "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
    #         "TimeInForce": "3",
    #         "OrdType": "D",
    #         "TransactTime": datetime.utcnow().isoformat(),
    #         "Price": quote_price if quote_price is not None else price,
    #         "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
    #         "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
    #         "NoLegs": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
    #         "QuoteID": quote.get_parameter("QuoteID")
    #     }
    #     super().change_parameters(base_parameters)
    #     return self
    #
    # def set_default_prev_quoted_swap_ndf_ccy2(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
    #                                           price: str = None, side: str = None):
    #     quote_price = None
    #     if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
    #         if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
    #             quote_price = quote.get_parameter("BidSwapPoints")
    #         else:
    #             quote_price = quote.get_parameter("OfferSwapPoints")
    #
    #     base_parameters = {
    #         "ClOrdID": bca.client_orderid(9),
    #         "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
    #         "HandlInst": "1",
    #         "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
    #         quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
    #         "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
    #         "TimeInForce": "3",
    #         "OrdType": "D",
    #         "TransactTime": datetime.utcnow().isoformat(),
    #         "Price": quote_price if quote_price is not None else price,
    #         "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
    #         "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
    #         "NoLegs": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
    #         "QuoteID": quote.get_parameter("QuoteID")
    #     }
    #     super().change_parameters(base_parameters)
    #     return self
    #
    # def set_default_for_dealer_swap(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
    #                                 price: str = None, side: str = None):
    #     quote_price = None
    #     if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
    #         if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
    #             quote_price = quote.get_parameter("OfferSwapPoints")
    #         else:
    #             quote_price = quote.get_parameter("BidSwapPoints")
    #
    #     base_parameters = {
    #         "ClOrdID": bca.client_orderid(9),
    #         "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
    #         "HandlInst": "1",
    #         "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
    #         quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
    #         "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
    #         "TimeInForce": "3",
    #         "OrdType": "D",
    #         "TransactTime": datetime.utcnow().isoformat(),
    #         "Price": quote_price if quote_price is not None else price,
    #         "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
    #         "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
    #         "NoLegs": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
    #         "QuoteID": quote.get_parameter("QuoteID")
    #     }
    #
    #     super().change_parameters(base_parameters)
    #     return self
