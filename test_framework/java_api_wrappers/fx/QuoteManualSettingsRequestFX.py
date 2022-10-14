from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteManualSettingsRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=QSMessageType.QuoteManualSettingsRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "QuoteManualSettingsRequestBlock": {
                "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                "ClientTierID": self.get_data_set().get_client_tier_id_by_name("client_tier_id_1"),
                "Tenor": self.get_data_set().get_tenor_java_api_by_name("tenor_spot"),
                "MDQuoteType": "TRD",
                "AutomatedMargin": "N"}}
        super().change_parameters(params_for_request)
        return self

    def set_executable_off(self):
        self.update_fields_in_component("QuoteManualSettingsRequestBlock", {"MDQuoteType": "IND"})
        return self

    def set_executable_on(self):
        self.update_fields_in_component("QuoteManualSettingsRequestBlock", {"MDQuoteType": "TRD"})
        return self

    def set_pricing_off(self):
        self.update_fields_in_component("QuoteManualSettingsRequestBlock",
                                        {"QuoteConditionList": {"QuoteConditionBlock": [
                                            {"QuoteConditionEnum": "CLO"}
                                        ]}})
        return self

    def set_pricing_on(self):
        self.remove_fields_from_component("QuoteManualSettingsRequestBlock", ["QuoteConditionList"])
        return self
