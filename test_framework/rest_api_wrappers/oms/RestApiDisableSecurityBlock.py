from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiDisableSecurityBlock(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("DisableSecurityBlock", data_set)
        self.base_parameters = {"prevClosePx": 10,
                                "listingID": 905,
                                "algoIncluded": 'True',
                                "instrID": "OqYEQbjef05OTF0ken9_qw",
                                "instrCurrency": "EUR",
                                "preferredVenueID": "PARIS",
                                "defaultMDSymbol": "905",
                                "currency": "EUR",
                                "symbol": "KFR",
                                "instrSymbol": "GB0033195214_EUR",
                                "securityID": "GB0033195214",
                                "securityIDSource": "ISI",
                                "lookupSymbol": "KFR.[PARIS]",
                                "ISINSecurityAltID": "GB0033195214",
                                "exchSymbSecurityAltID": "GB0033195214",
                                "securityExchange": "XLON",
                                "instrType": "EQU",
                                "orderBookVisibility": "V",
                                "venueID": "PARIS",
                                "preferredSecurityExchange": "XPAR",
                                "alive": True,
                                "listingDesc": [{"langCD": "en-US", "listingDescription": "KINGFISHER RGP"}],
                                "instrDesc": [{"instrLookupSymbol": "KFR", "instrDescription": "KINGFISHER RGP",
                                               "langCD": "en-US"}]}

    def set_default(self):
        self.set_params(self.base_parameters)

    def set_default_enable(self):
        self.message_type = 'EnableSecurityBlock'
        self.set_params(self.base_parameters)
        self.get_parameters()['alive'] = False
