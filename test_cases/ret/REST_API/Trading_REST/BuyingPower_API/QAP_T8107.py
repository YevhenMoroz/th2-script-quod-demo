import os

from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate


class QAP_T8107(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)

        # SAR
        self.tested_settl_currency = self.data_set.get_settl_currency_by_name('settl_currency_2')

        # api_cash_account_SAR
        self.tested_cash_account = self.data_set.get_cash_account_by_name('cash_account_2')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1, send submitNewOrderSimulate request and check SettlCurrBookedOrdAmt
        # cross-rate between SAR/INR
        self.noss_message.default_settl_currency_noss = self.tested_settl_currency
        self.noss_message.default_cash_account_noss = self.tested_cash_account
        self.noss_message.set_default_request()
        noss_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        data_validation(test_id=self.test_id,
                        event_name="Check SettlCurrBookedOrdAmt value",
                        expected_result=4,
                        actual_result=float(noss_response['SettlCurrBookedOrdAmt']))
        # endregion
