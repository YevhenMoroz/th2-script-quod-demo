from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyMarketMakingStatusMessages(RestApiMessages):

    def set_default_params(self):
        self.parameters = {
            "MDQuoteType": "TRD",
            "activeQuote": 'true',
            "marketMakingStatusID": '1'
        }
        self.message_type = 'ModifyMarketMakingStatus'
        return self

    def set_executable_enable(self):
        self.parameters.update({"MDQuoteType": "TRD"})
        return self

    def set_executable_disable(self):
        self.parameters.update({"MDQuoteType": "IND"})
        return self

    def set_pricing_enable(self):
        self.parameters.update({"activeQuote": "true"})
        return self

    def set_pricing_disable(self):
        self.parameters.update({"activeQuote": "false"})
        return self

