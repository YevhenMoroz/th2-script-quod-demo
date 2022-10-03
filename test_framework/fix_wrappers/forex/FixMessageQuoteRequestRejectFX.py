from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageQuoteRequestReject import FixMessageQuoteRequestReject
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuoteRequestRejectFX(FixMessageQuoteRequestReject):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)
        super().change_parameters(parameters)

    def set_quote_reject_params(self, quote_request: FixMessageQuoteRequestFX, text: str = None):
        quote_reject_params = {
            "QuoteReqID": quote_request.get_parameter("QuoteReqID"),
            "QuoteRequestRejectReason": "99",
            "NoRelatedSymbols": quote_request.get_parameter("NoRelatedSymbols"),
            "Text": text if text is not None else "*",

        }
        super().change_parameters(quote_reject_params)
        return self

    def set_deposit_reject_params(self, quote_request: FixMessageQuoteRequestFX, text: str = None):
        quote_reject_params = {
            "QuoteReqID": quote_request.get_parameter("QuoteReqID"),
            "QuoteRequestRejectReason": "3",
            "VenueType": "I",
            "Text": text if text is not None else "*",

        }
        super().change_parameters(quote_reject_params)
        return self

    def set_quote_reject_params_synergy(self, quote_request: FixMessageQuoteRequestFX, text: str = None):
        quote_reject_params = {
            "QuoteReqID": quote_request.get_parameter("QuoteReqID"),
            "QuoteRequestRejectReason": "3",
            "VenueType": quote_request.get_parameter("VenueType"),
            # "NoRelatedSymbols": quote_request.get_parameter("NoRelatedSymbols"),
            "Text": text if text is not None else "*",

        }
        super().change_parameters(quote_reject_params)
        return self