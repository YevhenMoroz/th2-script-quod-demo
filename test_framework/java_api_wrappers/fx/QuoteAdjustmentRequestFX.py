from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteAdjustmentRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=QSMessageType.QuoteAdjustmentRequest.value, data_set=data_set)
        super().change_parameters(parameters)
        self.params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteAdjustmentRequestBlock": {"QuoteAdjustmentEntryList": []
                                            },
            "InstrSymbol": "EUR/USD",
            "ClientTierID": "2800013",
            "Tenor": "SPO"}

    def set_empty_params(self):
        self.params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteAdjustmentRequestBlock": {"QuoteAdjustmentEntryList": []
                                            },
            "InstrSymbol": "EUR/USD",
            "ClientTierID": "2800013",
            "Tenor": "SPO"}
        return self

    def set_defaults(self):
        self.params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteAdjustmentRequestBlock": {
                "QuoteAdjustmentEntryList": {
                    "QuoteAdjustmentEntryBlock":
                        [{"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
                          "IndiceUpperQty": "1"},

                         {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
                          "IndiceUpperQty": "2"},

                         {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
                          "IndiceUpperQty": "3"}

                         ]},
                "InstrSymbol": "GBP/USD",
                "ClientTierID": "2800013",
                "Tenor": "SPO"}}

        super().change_parameters(self.params_for_request)
        return self

    def set_specific_bands_and_margins(self, bands: int, bid_margins: str = "0.1",
                                       offer_margins: str = "0.1"):
        for band in range(int(bands)):
            band += 1
            self.params_for_request["QuoteAdjustmentRequestBlock"]["QuoteAdjustmentEntryList"].append(
                {"BidMargin": str(bid_margins), "OfferMargin": str(offer_margins), "MDQuoteType": "TRD",
                 "IndiceUpperQty": band})
        return self

    def update_margins_by_index(self, index: int, bid_margin: str, offer_margin: str):
        self.params_for_request["QuoteAdjustmentRequestBlock"]["QuoteAdjustmentEntryList"]["QuoteAdjustmentEntryBlock"][
            index - 1].update(
            {"BidMargin": bid_margin, "OfferMargin": offer_margin, "MDQuoteType": "TRD",
             "IndiceUpperQty": index})
        return self

    def disable_pricing_by_index(self, index: int):
        self.params_for_request["QuoteAdjustmentRequestBlock"]["QuoteAdjustmentEntryList"][
            "QuoteAdjustmentEntryBlock"][index - 1].update(
            {"QuoteConditionList": {"QuoteConditionBlock":
                [{"QuoteConditionEnum": "Closed"}]
            }})
        return self

    def update_instrument(self, instrument: str):
        self.params_for_request["QuoteAdjustmentRequestBlock"].update({"InstrSymbol": instrument})
        return self

    def update_client_tier(self, clienttier: str):
        self.params_for_request["QuoteAdjustmentRequestBlock"].update({"ClientTierID": clienttier})
        return self

    def update_tenor(self, tenor: str):
        self.params_for_request["QuoteAdjustmentRequestBlock"].update({"Tenor": tenor})
        return self

    def change_subject(self, subject):
        self.change_parameter("SEND_SUBJECT", f"QUOD.{subject}.FE")
        self.change_parameter("REPLY_SUBJECT", f"QUOD.FE.{subject}")
        return self