from custom.tenor_settlement_date import wk1_ndf_maturity, wk2_ndf_maturity, wk3_ndf_maturity
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
            Account=quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
            OfferPx="*",
            OfferSize=quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"],
            ValidUntilTime="*",
            OfferSpotRate="*",
            OrigMDArrivalTime="*",
            OrigMDTime="*",
            OrigClientVenueID="*",
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            Product="4"),
            SettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"]
            if "SettlDate" in quote_request.get_parameter("NoRelatedSymbols")[0]
            else "*",
            SettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            Currency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            QuoteType=quote_request.get_parameter("NoRelatedSymbols")[0]["QuoteType"]
        )
        super().change_parameters(temp)
        return self

    def prepare_params_for_quote_ndf(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteMsgID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            Account=quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
            OfferPx="*",
            OfferSize=quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"],
            ValidUntilTime="*",
            OfferSpotRate="*",
            OrigMDArrivalTime="*",
            OrigMDTime="*",
            OrigClientVenueID="*",
            Instrument=dict(Symbol=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            MaturityDate="*"),
            SettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlDate"],
            SettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["SettlType"],
            Currency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            QuoteType=quote_request.get_parameter("NoRelatedSymbols")[0]["QuoteType"],
            OfferForwardPoints="*"
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

    def set_params_for_quote_ccy2(self, quote_request: FixMessageQuoteRequestFX):
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
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidPx": "*"})
            self.remove_parameter("OfferSpotRate")
            self.remove_parameter("OfferSize")
            self.remove_parameter("OfferPx")
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
            self.add_tag({"OfferPx": "*"})
            self.add_tag({"OfferSize": "*"})
            self.add_tag({"OfferSpotRate": "*"})
        return self

    def set_params_for_quote_ndf(self, quote_request: FixMessageQuoteRequestFX):
        self.prepare_params_for_quote_ndf(quote_request)
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

    def set_params_for_dealer_ccy2(self, quote_request: FixMessageQuoteRequestFX):
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
            self.add_tag({"Side": "1"})
            self.add_tag({"BidSpotRate": "*"})
            self.add_tag({"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["OrderQty"]})
            self.add_tag({"BidPx": "*"})
            self.remove_parameter("OfferSpotRate")
            self.remove_parameter("OfferSize")
            self.remove_parameter("OfferPx")
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
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
            self.remove_parameter("BidSpotRate")
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"BidForwardPoints": "*"})
            self.remove_parameter("OfferSpotRate")
        return self

    def set_params_for_dealer_fwd_ccy2(self, quote_request: FixMessageQuoteRequestFX):
        self.set_params_for_dealer(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidForwardPoints": "*"})
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"BidForwardPoints": "*"})
            self.remove_parameter("OfferSpotRate")
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"OfferForwardPoints": "*"})
            self.remove_parameter("BidSpotRate")
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

    def set_params_for_quote_fwd_ccy2(self, quote_request: FixMessageQuoteRequestFX):
        self.set_params_for_quote_ccy2(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidForwardPoints": "*"})
            self.add_tag({"OfferForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"BidForwardPoints": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"OfferForwardPoints": "*"})
        return self

    def prepare_params_for_swap(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteMsgID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            OfferPx="*",
            Currency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
            Account=quote_request.get_parameter("NoRelatedSymbols")[0]["Account"],
            ValidUntilTime="*",
            OfferSpotRate="*",
            BidSpotRate="*",
            QuoteType="1",
            OfferSwapPoints="*",
            OrigMDArrivalTime="*",
            OrigMDTime="*",
            OrigClientVenueID="*",
            NoLegs=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"],
            Instrument=dict(Symbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                            SecurityType=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                "SecurityType"],
                            Product="4"),
        )
        super().change_parameters(temp)
        return self

    def set_params_for_quote_swap(self, quote_request: FixMessageQuoteRequestFX, near_leg_bid_fwd_pts=None,
                                  near_leg_off_fwd_pts=None, far_leg_bid_fwd_pts=None, far_leg_off_fwd_pts=None,
                                  near_leg_bid_px=None, far_leg_off_px=None):
        temp = [dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSide"],
                     LegBidPx=near_leg_bid_px if near_leg_bid_px is not None else "*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlDate"],
                     LegOfferPx="*",
                     LegOfferForwardPoints=near_leg_off_fwd_pts if near_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=near_leg_bid_fwd_pts if near_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityExchange="*",
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
                         LegSecurityIDSource="*",
                     )
                     ),
                dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSide"],
                     LegBidPx="*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlDate"],
                     LegOfferPx=far_leg_off_px if far_leg_off_px is not None else "*",
                     LegOfferForwardPoints=far_leg_off_fwd_pts if far_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=far_leg_bid_fwd_pts if far_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegSecurityExchange="*",
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
                         LegSecurityIDSource="*",
                     )
                     )
                ]

        self.prepare_params_for_swap(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSwapPoints": "*"})
            self.add_tag({"BidPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"Side": "1"})
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"].split("/")[0] == \
                    quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"]:
                temp[0].pop('LegOfferPx')
                temp[0].pop('LegOfferForwardPoints')
                temp[1].pop('LegBidPx')
                temp[1].pop('LegBidForwardPoints')
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
            self.add_tag({"BidPx": "*"})
            self.add_tag({"BidSwapPoints": "*"})
            temp[0].pop('LegBidPx')
            temp[0].pop('LegBidForwardPoints')
            temp[1].pop('LegOfferPx')
            temp[1].pop('LegOfferForwardPoints')
            self.remove_parameters(["OfferPx", "OfferSwapPoints"])
        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[0]:
                temp[0].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[0]:
                temp[0].pop('LegBidForwardPoints')
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[1]:
                temp[1].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[1]:
                temp[1].pop('LegBidForwardPoints')

        self.update_repeating_group("NoLegs", temp)

        return self

    def set_params_for_quote_swap_ccy2(self, quote_request: FixMessageQuoteRequestFX, near_leg_bid_fwd_pts=None,
                                       near_leg_off_fwd_pts=None, far_leg_bid_fwd_pts=None, far_leg_off_fwd_pts=None,
                                       near_leg_off_px=None, far_leg_bid_px=None):
        temp = [dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSide"],
                     LegBidPx="*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlDate"],
                     LegOfferPx=near_leg_off_px if near_leg_off_px is not None else "*",
                     LegOfferForwardPoints=near_leg_off_fwd_pts if near_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=near_leg_bid_fwd_pts if near_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
                         LegSecurityExchange="*",
                         LegSecurityIDSource="*",
                     )
                     ),
                dict(LegSide=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSide"],
                     LegBidPx=far_leg_bid_px if far_leg_bid_px is not None else "*",
                     LegOrderQty=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegOrderQty"],
                     LegSettlDate=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlDate"],
                     LegOfferPx="*",
                     LegOfferForwardPoints=far_leg_off_fwd_pts if far_leg_off_fwd_pts is not None else "*",
                     LegBidForwardPoints=far_leg_bid_fwd_pts if far_leg_bid_fwd_pts is not None else "*",
                     LegSettlType=quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1][
                         "LegSettlType"],
                     InstrumentLeg=dict(
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
                         LegSecurityExchange="*",
                         LegSecurityIDSource="*",
                     )
                     )
                ]

        self.prepare_params_for_swap(quote_request)
        # self.add_tag({"Account": quote_request.get_parameter("NoRelatedSymbols")[0]["Account"]})
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSwapPoints": "*"})
            self.add_tag({"BidPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"].split("/")[0] != \
                    quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"]:
                temp[0].pop('LegOfferPx')
                temp[0].pop('LegOfferForwardPoints')
                temp[1].pop('LegBidPx')
                temp[1].pop('LegBidForwardPoints')
            else:
                temp[0].pop('LegBidPx')
                temp[0].pop('LegBidForwardPoints')
                temp[1].pop('LegOfferPx')
                temp[1].pop('LegOfferForwardPoints')
                self.add_tag({"BidSwapPoints": "*"})
                self.add_tag({"BidPx": "*"})
                self.remove_parameters(["OfferPx", "OfferSwapPoints"])
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"Side": "1"})
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"].split("/")[0] != \
                    quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"]:
                self.add_tag({"BidPx": "*"})
                self.add_tag({"BidSwapPoints": "*"})
                temp[0].pop('LegBidPx')
                temp[0].pop('LegBidForwardPoints')
                temp[1].pop('LegOfferPx')
                temp[1].pop('LegOfferForwardPoints')
                self.remove_parameters(["OfferPx", "OfferSwapPoints"])
            else:
                self.add_tag({"OfferPx": "*"})
                self.add_tag({"OfferSwapPoints": "*"})
                temp[0].pop('LegOfferPx')
                temp[0].pop('LegBidForwardPoints')
                temp[1].pop('LegBidPx')
                temp[1].pop('LegBidForwardPoints')
        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[0]:
                temp[0].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[0]:
                temp[0].pop('LegBidForwardPoints')
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[1]:
                temp[1].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[1]:
                temp[1].pop('LegBidForwardPoints')
        self.update_repeating_group("NoLegs", temp)

        return self

    def set_params_for_quote_swap_ndf(self, quote_request: FixMessageQuoteRequestFX, near_leg_bid_fwd_pts=None,
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
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
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
                         LegSymbol=(quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"],
                                    quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                                        "Symbol"] + "-SPO-QUODFX") if
                         quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0][
                             "LegSettlType"] == "0" else
                         quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"][
                             "Symbol"],
                         LegSecurityID=quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"],
                         LegCurrency=quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"],
                         LegSecurityExchange="*",
                         LegSecurityIDSource="*",
                     )
                     )
                ]

        self.prepare_params_for_swap(quote_request)
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.add_tag({"BidSwapPoints": "*"})
            self.add_tag({"BidPx": "*"})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.add_tag({"Side": "2"})
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"].split("/")[0] != \
                    quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"]:
                temp[0].pop('LegOfferPx')
                temp[0].pop('LegOfferForwardPoints')
                temp[1].pop('LegBidPx')
                temp[1].pop('LegBidForwardPoints')
            else:
                temp[0].pop('LegBidPx')
                temp[0].pop('LegBidForwardPoints')
                temp[1].pop('LegOfferPx')
                temp[1].pop('LegOfferForwardPoints')
                self.add_tag({"BidSwapPoints": "*"})
                self.add_tag({"BidPx": "*"})
                self.remove_parameters(["OfferPx", "OfferSwapPoints"])
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.add_tag({"Side": "1"})
            if quote_request.get_parameter("NoRelatedSymbols")[0]["Instrument"]["Symbol"].split("/")[0] != \
                    quote_request.get_parameter("NoRelatedSymbols")[0]["Currency"]:
                self.add_tag({"BidPx": "*"})
                self.add_tag({"BidSwapPoints": "*"})
                temp[0].pop('LegBidPx')
                temp[0].pop('LegOfferForwardPoints')
                temp[1].pop('LegOfferPx')
                temp[1].pop('LegOfferForwardPoints')
                self.remove_parameters(["OfferPx", "OfferSwapPoints"])
            else:
                self.add_tag({"OfferPx": "*"})
                self.add_tag({"OfferSwapPoints": "*"})
                temp[0].pop('LegOfferPx')
                temp[0].pop('LegBidForwardPoints')
                temp[1].pop('LegBidPx')
                temp[1].pop('LegBidForwardPoints')
        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[0]:
                temp[0].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[0]:
                temp[0].pop('LegBidForwardPoints')
        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "0":
            if "LegOfferForwardPoints" in temp[1]:
                temp[1].pop('LegOfferForwardPoints')
            if "LegBidForwardPoints" in temp[1]:
                temp[1].pop('LegBidForwardPoints')

        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "W1":
            temp[0]["InstrumentLeg"]["LegMaturityDate"] = wk1_ndf_maturity()
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "W2":
            temp[0]["InstrumentLeg"]["LegMaturityDate"] = wk2_ndf_maturity()
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] == "W3":
            temp[0]["InstrumentLeg"]["LegMaturityDate"] = wk3_ndf_maturity()

        if quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "W1":
            temp[1]["InstrumentLeg"]["LegMaturityDate"] = wk1_ndf_maturity()
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "W2":
            temp[1]["InstrumentLeg"]["LegMaturityDate"] = wk2_ndf_maturity()
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] == "W3":
            temp[1]["InstrumentLeg"]["LegMaturityDate"] = wk3_ndf_maturity()

        self.update_repeating_group("NoLegs", temp)

        return self

    def prepare_params_for_deposit_and_loan(self, quote_request: FixMessageQuoteRequestFX):
        temp = dict(
            QuoteID="*",
            QuoteReqID=quote_request.get_parameter("QuoteReqID"),
            OfferPx="*",
            BidPx="*",
            VenueType="*",
            NoPartyIDs="*",
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
