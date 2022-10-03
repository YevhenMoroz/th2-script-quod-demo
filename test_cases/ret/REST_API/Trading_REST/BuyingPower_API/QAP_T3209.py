import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import \
    RestApiCashAccountMessages
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager


class QAP_T3209(TestCase):
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
        self.buying_power_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=data_set)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.cash_account_message = RestApiCashAccountMessages(data_set=data_set)
        self.security_account_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        self.cash_account_id = self.data_set.get_cash_account_counters_by_name('cash_account_counter_1')
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region Pre-Condition, create new order with side=Buy
        self.nos_message.set_default_request()
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region Pre-Condition, get new security position
        self.security_account_position_message.find_positions(
            security_account_name=self.nos_message.default_account_nos)
        new_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.instrument_id})
        print(new_position)
        # endregion

        # region Pre-Condition, set new InitialQty and ReservedQty value for created position and check result
        try:
            new_position[0].update({'initialQty': 10000})
            new_position[0].update({'reservedQty': 20})
            self.security_account_position_message.modify_security_positions(params=new_position[0])
        except(KeyError, TypeError, IndexError):
            bca.create_event(f'Response is empty new position was not created', status='FAILED', parent_id=self.test_id)
        self.wa_api_manager.send_post_request(self.security_account_position_message)

        self.security_account_position_message.find_positions(self.nos_message.default_account_nos)
        modified_security_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.instrument_id})

        data_validation(test_id=self.test_id,
                        event_name="Check that initialQty equal 10000.0",
                        expected_result="10000.0",
                        actual_result=modified_security_position[0]['initialQty'])
        data_validation(test_id=self.test_id,
                        event_name="Check that reservedQty equal 20.0",
                        expected_result="20.0",
                        actual_result=modified_security_position[0]['reservedQty'])
        # endregion

        # region, send requests: findCashAccountCounters, submitNewOrderSingleSimulate and check correct calculation
        self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)
        cash_positions = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))

        self.noss_message.set_default_request()
        noss_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        print(cash_positions[0])
        print(modified_security_position[0])

        buying_power = self.buying_power_manager.calc_buying_power(test_id=self.test_id,
                                                                   response_wa_cash_account=cash_positions[0],
                                                                   response_wa_security_account=
                                                                   modified_security_position[0])

        data_validation(test_id=self.test_id,
                        event_name="Check that 'BuyingPower' value is calculated correctly",
                        expected_result=buying_power,
                        actual_result=float(noss_response['BuyingPowerLimitAmt']))
        # endregion
