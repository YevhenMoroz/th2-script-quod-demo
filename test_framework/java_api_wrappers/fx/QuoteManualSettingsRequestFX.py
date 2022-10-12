from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteManualSettingsRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=QSMessageType.QuoteManualSettingsRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_defaults(self):
        params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteManualSettingsRequestBlock": {
                "InstrSymbol": "EUR/USD",
                "ClientTierID": "2200009",
                "Tenor": "SPO",
                "MDQuoteType": "TRD",
                "AutomatedMargin": "N"}}
        super().change_parameters(params_for_request)

    def turn_pricing_off(self):
        self.change_parameter("QuoteManualSettingsRequestBlock", {
            "InstrSymbol": "EUR/USD",
            "ClientTierID": "2200009",
            "Tenor": "SPO",
            "MDQuoteType": "TRD",
            "AutomatedMargin": "N",
            "QuoteConditionList":
                {"QuoteConditionBlock": [
                    {"QuoteConditionEnum": "CLO"}
                ]}})

    def turn_executable_off(self):
        self.change_parameter("QuoteManualSettingsRequestBlock", {
            "InstrSymbol": "EUR/USD",
            "ClientTierID": "2200009",
            "Tenor": "SPO",
            "MDQuoteType": "IND",
            "AutomatedMargin": "N"
                })

# "QuoteAdjustmentEntryList": {
#                     "QuoteAdjustmentEntryBlock":
#                         [{"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
#                           "IndiceUpperQty": "1"},
#
#                          {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
#                           "IndiceUpperQty": "2"},
#
#                          {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
#                           "IndiceUpperQty": "3"}
#
#                          ]}
