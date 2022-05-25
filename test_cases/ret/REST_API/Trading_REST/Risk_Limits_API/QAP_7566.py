import os

from test_cases.wrapper.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import RestApiCashAccountMessages
from test_framework.rest_api_wrappers.BuyingPowerFormulasManager import BuyingPowerFormulasManager


class QAP_7566(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.web_admin = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.web_admin, case_id=self.test_id)
        self.buying_power_manager = BuyingPowerFormulasManager()
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.cash_account_message = RestApiCashAccountMessages(data_set=data_set)
        self.tested_currency = self.data_set.get_currency_by_name('currency_1')
        self.tested_client = self.data_set.get_client_by_name('client_4')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region, send requests: findCashAccountCounters, submitNewOrderSingleSimulate and check correct calculation
        self.cash_account_message.find_cash_account_counters(client_name=self.tested_client,
                                                             currency=self.tested_currency)
        cash_positions = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))
        self.noss_message.set_default_request()
        noss_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        try:
            buying_power = self.buying_power_manager.calc_buying_power(response_wa=cash_positions[0],
                                                                       response_trd=noss_response)
            verifier(case_id=self.test_id,
                     event_name="Check that 'BuyingPower' value is calculated correctly",
                     expected_value=buying_power,
                     actual_value=float(noss_response['BuyingPowerLimitAmt']))
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
