import os

from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.BuyingPowerFormulasManager import BuyingPowerFormulasManager


class QAP_7670(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.web_admin = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.buying_power_manager = BuyingPowerFormulasManager()
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region step 2, send submitNewOrderSingleSimulate side=Buy request and check CashBalance calculation with
        self.noss_message.set_default_request()
        noss_response_buy = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        try:
            cash_balance_buy = self.buying_power_manager.calc_cash_balance(noss_response_buy, side='Buy')
            verifier(case_id=self.test_id,
                     event_name="Check that 'CashBalance' value is calculated correctly with side=Buy",
                     expected_value=cash_balance_buy,
                     actual_value=float(noss_response_buy['CashBalance']))
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion

        # region step 3, send submitNewOrderSingleSimulate with side=Sell request and check CashBalance calculation
        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        noss_response_sell = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        try:
            cash_balance_sell = self.buying_power_manager.calc_cash_balance(noss_response_sell, side='Sell')
            verifier(case_id=self.test_id,
                     event_name="Check that 'CashBalance' value is calculated correctly with side=Sell",
                     expected_value=cash_balance_sell,
                     actual_value=float(noss_response_sell['CashBalance']))
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty', status='FAILED', parent_id=self.test_id)
        # endregion
