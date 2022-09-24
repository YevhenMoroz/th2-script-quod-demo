import os

from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.cum_trading_limit_counter_api.RestApiCumTradingLimitCounter import RestApiCumTradingLimitCounter


class QAP_T3505(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.web_admin = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.web_admin, case_id=self.test_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.cum_trading_limit_counter = RestApiCumTradingLimitCounter(data_set=data_set)
        self.error_message = "11824 &apos;Calculated CumLeavesOrdAmt&apos; (200) greater than MaxCumLeavesOrdAmt (100)"
        self.client = self.data_set.get_client_by_name('client_7')
        self.account = self.data_set.get_account_by_name('account_7')
        self.cash_account = self.data_set.get_cash_account_by_name('cash_account_4')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send new order and verify result
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=100)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocQty': 100})
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocClientAccountID': self.account})
        self.nos_message.change_parameter(parameter_name='ClientAccountGroupID', new_parameter_value=self.client)
        self.nos_message.change_parameter(parameter_name='ClientCashAccountID', new_parameter_value=self.cash_account)
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        self.cum_trading_limit_counter.find_all_cum_trading_limit_counters()
        cum_trd_limit_counter = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.cum_trading_limit_counter))
        data_validation(test_id=self.test_id,
                        event_name="Check that User can send order with Amt = the sum of 'Max Open Order Amount' for open orders",
                        expected_result='100.0',
                        actual_result=cum_trd_limit_counter[0]['cumOrdAmt'])

