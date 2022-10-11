from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiBuyingPowerMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def find_all_buying_power_limit(self):
        self.message_type = "FindAllBuyingPowerLimit"

    def create_buying_power(self, custom_params=None):
        self.message_type = "CreateBuyingPowerLimit"
        default_parameters = (
            {
                "buyingPowerLimitName": "api_bp_rule",
                "disallowSameListing": "true",
                "includeCash": "true",
                "disallowDelivContracts": "true",
                "buyingPowerRefPriceType": "LTP",
                "includeCollateralCash": "true",
                "holdingsRatio": 4,
                "includeSecurities": "true",
                "buyingPowerLimitDesc": "api_bp_rule",
                "includeCashLoan": "true",
                "includeTempCash": "true",
                "allowCashOnNegativeLedger": "true",
                "allowSecuritiesOnNegLedger": "true"
            }
        )
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

