from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiManageSecurityBlock(RestApiMessages):
    def __init__(self, data_set: BaseDataSet):
        super().__init__("ManageSecurityBlock", data_set)
        self.base_parameters = {"listingID": "9500000049",
                                "algoIncluded": "true",
                                "instrID": "JAFGYQq-9qTrmmY9kyM2TQ",
                                "instrCurrency": "GBp",
                                "preferredVenueID": "EUREX",
                                "tickSizeProfileID": 3,
                                "currency": "GBp",
                                "symbol": "EUR",
                                "instrSymbol": "IS3",
                                "securityID": "ISI3",
                                "securityIDSource": "ISI",
                                "lookupSymbol": "EUR[EUREX]",
                                "ISINSecurityAltID": "IS0000000001",
                                "exchSymbSecurityAltID": "IS0000000001",
                                "securityExchange": "XEUR",
                                "instrType": "EQU",
                                "orderBookVisibility": "V",
                                "venueID": "EUREX",
                                "preferredSecurityExchange": "XEUR",
                                "alive": "true"}

    def set_default_param(self):
        self.set_params(self.base_parameters)
        return self

    def set_fee_exemption(self, stamp=False, levy=False, per_transac=False):
        self.set_params(self.base_parameters)
        if stamp: self.change_params({"stampFeeExemption": "true"})
        if levy: self.change_params({"levyFeeExemption": "true"})
        if per_transac: self.change_params({"perTransacFeeExemption": "true"})
        return self
