from test_framework.data_sets.constants import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuoteFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.Quote.value)
        super().change_parameters(parameters)

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
            QuoteType=quote_request.get_parameter("NoRelatedSymbols")[0]["QuoteType"]
        )
        super().change_parameters(temp)
        return self

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

    def set_params_for_dealer(self, quote_request: FixMessageQuoteRequestFX):
        self.prepare_params_for_quote(quote_request)
        self.remove_parameters(["SettlType", "SettlDate", "QuoteType"])
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidPx": "*"})
            self.add_tag({"OfferSpotRate": "*"})
            self.add_tag({"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"OfferPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidPx": "*"})
            self.add_tag({"OfferPx": "*"})
            self.add_tag({"OfferSize": "*"})
            self.add_tag({"OfferSpotRate": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidPx": "*"})
            self.add_tag({"OfferPx": "*"})
            self.add_tag({"OfferSize": "*"})
            self.add_tag({"OfferSpotRate": "*"})
        return self

    def set_params_for_dealer_fwd(self, quote_request: FixMessageQuoteRequestFX):
        self.set_params_for_dealer(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidForwardPoints": "*"})
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"BidForwardPoints": "*"})
        return self

    def set_params_for_quote_fwd(self, quote_request: FixMessageQuoteRequestFX):
        self.set_params_for_quote(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidForwardPoints": "*"})
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"BidForwardPoints": "*"})
        return self

    def prepare_params_for_swap(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteMsgID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            OfferPx="*",
            OfferSize=quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"],
            Currency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            ValidUntilTime="*",
            OfferSpotRate="*",
            BidSpotRate="*",
            QuoteType="1",
            OfferSwapPoints="*",
            NoLegs=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            Product="4"),
        )
        super().change_parameters(temp)
        return self

    def set_params_for_quote_swap(self, quote_request: FixMessageQuoteRequestFX, near_leg_bid_fwd_pts=None,
                                  near_leg_off_fwd_pts=None, far_leg_bid_fwd_pts=None, far_leg_off_fwd_pts=None):
        temp = [dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSide"],
                     LegBidPx="*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlDate"],
                     LegOfferPx="*",
                     LegOfferForwardPoints=near_leg_off_fwd_pts if near_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=near_leg_bid_fwd_pts if near_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityExchange="*",
                         LegSecurityIDSource="*",
                     )
                     ),
                dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSide"],
                     LegBidPx="*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlDate"],
                     LegOfferPx="*",
                     LegOfferForwardPoints=far_leg_off_fwd_pts if far_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=far_leg_bid_fwd_pts if far_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityExchange="*",
                         LegSecurityIDSource="*",
                     )
                     )
                ]
        self.prepare_params_for_swap(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSwapPoints": "*"})
            self.add_tag({"BidSize": "*"})
            self.add_tag({"BidPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"Side": "1"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "0":
            temp[0].pop('LegOfferForwardPoints')
            temp[0].pop('LegBidForwardPoints')
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "0":
            temp[1].pop('LegOfferForwardPoints')
            temp[1].pop('LegBidForwardPoints')
        self.update_repeating_group("NoLegs", temp)

        return self

    def prepare_params_for_deposit_and_loan(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            OfferPx="*",
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSym")[0]["Instrument"]["Symbol"],
                            Product=quote_request.get_parameter("NoRelatedSym")[0]["Instrument"]["Product"])

        )
        super().change_parameters(temp)
        return self

    def set_params_for_deposit_and_loan(self, quote_request: FixMessageQuoteRequestFX):
        self.prepare_params_for_deposit_and_loan(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSym")[0]:
            self.add_tag({"BidPx": "*"})
            self.add_tag({"OfferPx": "*"})
        elif quote_request.get_parameter("NoRelatedSym")[0]["Side"] == "1":
            self.remove_parameter("BidPx")
        elif quote_request.get_parameter("NoRelatedSym")[0]["Side"] == "2":
            self.remove_parameter("OfferPx")
        return self
