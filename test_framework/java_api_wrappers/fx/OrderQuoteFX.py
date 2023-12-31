from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.ors_messages.QuoteRequestActionReply import QuoteRequestActionReply
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class OrderQuoteFX(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=QSMessageType.Quote.value)
        super().change_parameters(parameters)

    # region Quotes
    def prepare_params(self, action_reply: QuoteRequestActionReply):
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        params_for_request = {
            "SEND_SUBJECT": "QUOD.QS_RFQ_FIX_TH2.FE",
            "REPLY_SUBJECT": "QUOD.FE.QS_RFQ_FIX_TH2",
            "QuoteBlock": {
                "QuoteRequestID": action_reply.get_parameter("QuoteRequestActionReplyBlock")["QuoteRequestID"],
                "InstrID": estimation_block["InstrID"],
                "ListingID": estimation_block["ListingID"],
                "AccountGroupID": estimation_block["AccountGroupID"],
                "QuoteTTL": "120",
                "AutomaticHedging": "Y",
            }
        }

        super().change_parameters(params_for_request)
        return self

    def set_params_for_quote(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReply):
        self.prepare_params(action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": "0"})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": "0"})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        return self

    def set_params_for_quote_synergy(self, quote_request: FixMessageQuoteRequestFX,
                                     action_reply: QuoteRequestActionReply):
        self.prepare_params(action_reply)
        self.change_parameter("SEND_SUBJECT", "QUOD.QS_RFQ_FIX_CNX_TH2.FE")
        self.change_parameter("REPLY_SUBJECT", "QUOD.FE.QS_RFQ_FIX_CNX_TH2")
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSym")[0]:
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSym")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": "0"})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": "0"})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSym")[0][
                                                "OrderQty"]})
        return self

    def set_params_for_swap_quote(self, quote_request: FixMessageQuoteRequestFX,
                                  action_reply: QuoteRequestActionReply):
        self.prepare_params(action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": "0"})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"]
                                            [0]["LegOrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"]
                                            [1]["LegOrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"OfferPx": "0"})
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "LegOrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "LegOrderQty"]})
        return self

    def set_params_for_quote_ccy2(self, quote_request: FixMessageQuoteRequestFX,
                                  action_reply: QuoteRequestActionReply):
        self.prepare_params(action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock", {"BidPx": "0"})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
            self.update_fields_in_component("QuoteBlock", {"OfferPx": "0"})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"BidPx": "0"})
            self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"BidSize": quote_request.get_parameter("NoRelatedSymbols")[0][
                                                "OrderQty"]})
        return self

    def set_params_for_fwd(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReply):
        self.set_params_for_quote(quote_request, action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferForwardPoints": estimation_block["OfferForwardPoints"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferForwardPoints": estimation_block["OfferForwardPoints"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})

    def set_params_for_fwd_ccy2(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReply):
        self.set_params_for_quote_ccy2(quote_request, action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
            self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferForwardPoints": estimation_block["OfferForwardPoints"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
            self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
            self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})
        elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
            self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
            self.update_fields_in_component("QuoteBlock",
                                            {"OfferForwardPoints": estimation_block["OfferForwardPoints"]})

    # endregion Quotes
    # region Swaps
    def prepare_params_swap(self, action_reply: QuoteRequestActionReply):
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        params_for_request = {
            "SEND_SUBJECT": "QUOD.QS_RFQ_FIX_TH2.FE",
            "REPLY_SUBJECT": "QUOD.FE.QS_RFQ_FIX_TH2",
            "QuoteBlock": {
                "QuoteRequestID": action_reply.get_parameter("QuoteRequestActionReplyBlock")["QuoteRequestID"],
                "InstrID": estimation_block["InstrID"],
                "ListingID": estimation_block["ListingID"],
                "AccountGroupID": estimation_block["AccountGroupID"],
                "QuoteTTL": "120",
                "AutomaticHedging": "Y",
                "LegQuoteList": {
                    "LegQuoteBlock": [
                        {}, {}
                    ]}
            }
        }

        super().change_parameters(params_for_request)
        return self

    def set_params_for_swap_for_dealer(self, quote_request: FixMessageQuoteRequestFX,
                                       action_reply: QuoteRequestActionReply):
        self.prepare_params_swap(action_reply)

    def set_params_for_swap(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReply):
        self.prepare_params_swap(action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        reply_leg_quote_block = estimation_block["LegQuoteList"]["LegQuoteBlock"]
        self.update_fields_in_component("QuoteBlock", {"AutomaticHedging": "N"})
        self.get_parameter("QuoteBlock")["LegQuoteList"]["LegQuoteBlock"][0] = reply_leg_quote_block[0]
        self.get_parameter("QuoteBlock")["LegQuoteList"]["LegQuoteBlock"][1] = reply_leg_quote_block[1]
        self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
        self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
        self.update_fields_in_component("QuoteBlock", {"BidSwapPoints": estimation_block["BidSwapPoints"]})
        self.update_fields_in_component("QuoteBlock", {"OfferSwapPoints": estimation_block["OfferSwapPoints"]})
        self.update_fields_in_component("QuoteBlock", {"OfferPx": estimation_block["OfferPx"]})
        self.update_fields_in_component("QuoteBlock", {"BidPx": estimation_block["BidPx"]})
        # self.update_fields_in_component("QuoteBlock", {"QuoteType": "1"})

        # if "Side" not in quote_request.get_parameter("NoRelatedSymbols")[0]:
        #     self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
        #     self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
        #     self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})
        #     self.update_fields_in_component("QuoteBlock",
        #                                     {"OfferForwardPoints": estimation_block["OfferForwardPoints"]})
        # elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "1":
        #     self.update_fields_in_component("QuoteBlock", {"OfferSpotRate": estimation_block["OfferSpotRate"]})
        #     self.update_fields_in_component("QuoteBlock",
        #                                     {"OfferForwardPoints": estimation_block["OfferSwapPoints"]})
        # elif quote_request.get_parameter("NoRelatedSymbols")[0]["Side"] == "2":
        #     self.update_fields_in_component("QuoteBlock", {"BidSpotRate": estimation_block["BidSpotRate"]})
        #     self.update_fields_in_component("QuoteBlock", {"BidForwardPoints": estimation_block["BidForwardPoints"]})
    # endregion
