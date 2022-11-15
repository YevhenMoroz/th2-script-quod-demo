from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiAlgoPolicyMessages(RestApiMessages):

    def find_all_algo_policies(self):
        """
        This method return all algo policies(strategies)
        """
        self.message_type = 'FindAllAlgoPolicy'
        return self

    def modify_algo_policy(self, parameters):
        """
        This method modify exist
        """
        self.message_type = 'ModifyAlgoPolicy'
        self.parameters = parameters
        return self

    def find_all_trading_phase_profile(self):
        self.message_type = 'FindAllTradingPhaseProfile'
        return self


