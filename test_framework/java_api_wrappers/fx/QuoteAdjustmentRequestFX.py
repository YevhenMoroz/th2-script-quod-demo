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
            "InstrSymbol": "EUR/PHP",
            "ClientTierID": "2800013",
            "Tenor": "SPO"}

    def set_default_params(self):
        self.params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteAdjustmentRequestBlock": {"QuoteAdjustmentEntryList": {
                "QuoteAdjustmentEntryBlock":
                    [{"BidMargin": "-0.1", "OfferMargin": "0.1", "MDQuoteType": "TRD",
                      "IndiceUpperQty": "1"},

                     {"BidMargin": "-0.1", "OfferMargin": "0.1", "MDQuoteType": "TRD",
                      "IndiceUpperQty": "2"},

                     {"BidMargin": "-0.1", "OfferMargin": "0.1", "MDQuoteType": "TRD",
                      "IndiceUpperQty": "3"}

                     ]},
                "InstrSymbol": "GBP/USD",
                "ClientTierID": "2800013",
                "Tenor": "SPO"}}

        super().change_parameters(self.params_for_request)

    def set_specific_bands_and_margins(self, bands: str, bid_margins: str = "0.1",
                                       offer_margins: str = "0.1"):
        for band in range(int(bands)):
            band += 1
            self.params_for_request["QuoteAdjustmentRequestBlock"]["QuoteAdjustmentEntryList"].append(
                {"BidMargin": str(bid_margins), "OfferMargin": str(offer_margins), "MDQuoteType": "TRD",
                 "IndiceUpperQty": band})

    def change_subject(self, subject):
        self.change_parameter("SEND_SUBJECT", f"QUOD.{subject}.FE")
        self.change_parameter("REPLY_SUBJECT", f"QUOD.FE.{subject}")
