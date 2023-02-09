from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.fx.QuoteRequestActionReplyFX import QuoteRequestActionReplyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class OrderQuoteFX(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=QSMessageType.Quote.value)
        super().change_parameters(parameters)

    # region Quotes
    def prepare_params(self, action_reply: QuoteRequestActionReplyFX):
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

    def set_params_for_quote(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReplyFX):
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

    def set_params_for_quote_ccy2(self, quote_request: FixMessageQuoteRequestFX,
                                  action_reply: QuoteRequestActionReplyFX):
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

    def set_params_for_fwd(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReplyFX):
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

    def set_params_for_fwd_ccy2(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReplyFX):
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
    def set_params_for_swap(self, quote_request: FixMessageQuoteRequestFX, action_reply: QuoteRequestActionReplyFX):
        self.prepare_params(action_reply)
        estimation_block = action_reply.get_parameter("QuoteRequestActionReplyBlock")["EstimatedQuoteBlock"]
        leg_quote_block = estimation_block["LegQuoteList"]["LegQuoteBlock"]

    # endregion
