import os

from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager


class QAP_T3260(TestCase):
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
        self.security_account_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        # "api_account_rin_desk"
        self.tested_security_account = self.data_set.get_account_by_name('account_4')
        # InstrSymbol="TASI"
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name('instrument_3')
        # "_kRAMqAgQauzyJvU7V6R9w"
        self.tested_instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_3')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-Condition, create new order with side=Buy
        self.nos_message.tested_instrument_nos = self.tested_instrument
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=10)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations', fields={'AllocQty': 10})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region Pre-Condition, check that new position is created
        self.security_account_position_message.find_positions(security_account_name=self.tested_security_account)
        new_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})
        # endregion

        # region Pre-Condition, set new InitialQty value for created position and check result
        try:
            new_position[0].update({'initialQty': 10000})
            self.security_account_position_message.modify_security_positions(params=new_position[0])
        except:
            bca.create_event(f'Response is empty new position was not created', status='FAILED', parent_id=self.test_id)

        self.wa_api_manager.send_post_request(self.security_account_position_message)

        self.security_account_position_message.find_positions(self.tested_security_account)
        modified_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})
        try:
            verifier(case_id=self.test_id,
                     event_name="Check that initialQty equal 10000.0",
                     expected_value="10000.0",
                     actual_value=modified_position[0]['initialQty'])
        except:
            bca.create_event(f'Response is empty, initialQty cannot be verified', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Steps 1,2,3,4,5 Check Total Position Qty
        try:
            total_posit_qty = self.buying_power_manager.calc_total_posit_qty(self.test_id, modified_position[0], 10)

            if total_posit_qty >= 0:
                bca.create_event(f'Total Position Qty >= 0', status='SUCCESS', parent_id=self.test_id)
            elif total_posit_qty < 0:
                bca.create_event(f'Total Position Qty < 0', status='FAILED', parent_id=self.test_id)
        except:
            bca.create_event(f'Response is empty, steps 1-5', status='FAILED', parent_id=self.test_id)
        # endregion

        # region Step 6, create new order with side=Sell
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=10)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations', fields={'AllocQty': 10})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region Step 7, Check that reservedQty was increased
        self.security_account_position_message.find_positions(security_account_name=self.tested_security_account)
        new_leaves_sell_qty = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})

        try:
            verifier(case_id=self.test_id,
                     event_name="Check that leavesSellQty was increased by 10",
                     expected_value=float(modified_position[0]['leavesSellQty']) + 10,
                     actual_value=float(new_leaves_sell_qty[0]['leavesSellQty']))
        except:
            bca.create_event(f'Response is empty, step 7', status='FAILED', parent_id=self.test_id)
        # endregion
