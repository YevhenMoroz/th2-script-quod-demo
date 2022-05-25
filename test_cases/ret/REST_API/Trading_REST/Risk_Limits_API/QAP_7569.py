import os

from test_cases.wrapper.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate


class QAP_7569(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1, send submitNewOrderSimulate request and check that SettlCurrBookedOrdAmt equal 1
        # cross-rate between INR/INR
        self.noss_message.set_default_request()
        parsed_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        try:
            verifier(case_id=self.test_id,
                     event_name="Check that SettlCurrBookedOrdAmt = 1",
                     expected_value=1,
                     actual_value=float(parsed_response['SettlCurrBookedOrdAmt']))
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
        