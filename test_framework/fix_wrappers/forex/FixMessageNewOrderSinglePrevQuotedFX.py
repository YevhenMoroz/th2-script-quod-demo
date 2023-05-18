from datetime import datetime
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.forex import FixMessageQuoteFX, FixMessageQuoteRequestFX


class FixMessageNewOrderSinglePrevQuotedFX(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_default_prev_quoted(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                                price: str = None,
                                side: str = None) -> FixMessageNewOrderSingle:
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
            "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_prev_quoted_ccy2(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                                     price: str = None,
                                     side: str = None) -> FixMessageNewOrderSingle:
        quote_price = None
        if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
            if quote.get_parameter("Side") == "1":
                quote_price = quote.get_parameter("BidPx")
            else:
                quote_price = quote.get_parameter("OfferPx")

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
            "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_for_dealer(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                               price: str = "1.184",
                               side: str = "1") -> FixMessageNewOrderSingle:
        quote_price = None
        if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
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
            "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_for_dealer_ccy2(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                                    price: str = "1.184",
                                    side: str = "1") -> FixMessageNewOrderSingle:
        quote_price = None
        if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
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
            "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_for_dealer_swap(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                               price: str = "1.184",
                               side: str = "1") -> FixMessageNewOrderSingle:
        quote_price = None
        # if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
        #     if quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
        #         quote_price = quote.get_parameter("OfferPx")
        #     else:
        #         quote_price = quote.get_parameter("BidPx")

        base_parameters = {
            "ClOrdID": bca.client_orderid(9),
            "Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
            "HandlInst": "1",
            "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
            quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
            "OrderQty": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
            "TimeInForce": "3",
            "OrdType": "D",
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": quote_price if quote_price is not None else price,
            # "Currency": quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            # "Instrument": quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"],
            # "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            # "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            # "QuoteID": quote.get_parameter("QuoteID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_deposit_and_loan(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                                     price: str = None,
                                     side: str = None) -> FixMessageNewOrderSingle:
        # quote_price = None
        # if "Side" in quote_request.get_parameter("NoRelatedSymbols")[0]:
        #     if quote.get_parameter("Side") == "1":
        #         quote_price = quote.get_parameter("OfferPx")
        #     else:
        #         quote_price = quote.get_parameter("BidPx")
        base_parameters = {
            "ClOrdID": bca.client_orderid(15),
            "SecondaryClOrdID": quote.get_parameter("QuoteReqID"),
            # "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0] else
            # quote_request.get_parameter("NoRelatedSymbols")[0]["Side"],
            "Side": "2",
            "OrderQty": quote_request.get_parameter("NoRelatedSym")[0]["OrderQty"],
            "OrdType": "D",
            "NoPartyIDs": [
                {
                    "PartyID": "CLIENT1",
                    "PartyIDSource": "D",
                    "PartyRole": "1"
                }
            ],
            "TransactTime": datetime.utcnow().isoformat(),
            # "Price": quote_price if quote_price is not None else price,
            "Instrument": quote_request.get_parameter("NoRelatedSym")[0]["Instrument"],
            # "SettlDate": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            # "SettlType": quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            "QuoteID": quote.get_parameter("QuoteID") # "QuoteID": quote.get_parameter("QuoteReqID")
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_synergy(self, quote_request: FixMessageQuoteRequestFX, quote: FixMessageQuoteFX,
                                     price: str = None,
                                     side: str = None) -> FixMessageNewOrderSingle:
        quote_price = None
        if "Side" in quote_request.get_parameter("NoRelatedSym")[0]:
            if quote.get_parameter("Side") == "1":
                quote_price = quote.get_parameter("OfferPx")
            else:
                quote_price = quote.get_parameter("BidPx")

        base_parameters = {
            "ClOrdID": bca.client_orderid(9),
            "SecondaryClOrdID": bca.client_orderid(9),
            "Side": side if "Side" not in quote_request.get_parameter("NoRelatedSym")[0] else
            quote_request.get_parameter("NoRelatedSym")[0]["Side"],
            "OrderQty": quote_request.get_parameter("NoRelatedSym")[0]["OrderQty"],
            "TimeInForce": "3",
            "OrdType": "D",
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": quote_price if quote_price is not None else price,
            "Currency": quote_request.get_parameter("NoRelatedSym")[0]["Currency"],
            "Instrument": quote_request.get_parameter("NoRelatedSym")[0]["Instrument"],
            "SettlDate": quote_request.get_parameter("NoRelatedSym")[0]["SettlDate"],
            "NoPartyIDs": quote_request.get_parameter("NoRelatedSym")[0]["NoPartyIDs"],
            "QuoteID": quote.get_parameter("QuoteID"),
            "VenueType": quote.get_parameter("VenueType")
        }
        instrument = dict(
            SecurityType="FOR",
            Symbol=quote_request.get_parameter("NoRelatedSym")[0]["Instrument"]["Symbol"],
            Product="4",
        )
        super().change_parameters(base_parameters)
        super().update_fields_in_component("Instrument", instrument)
        return self

