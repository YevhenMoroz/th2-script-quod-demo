import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3140(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.formulas_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.security_account_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        # TCS-IQ[NSE]
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        # ePKRr68Nr7pDFdVkx6amaQ
        self.tested_instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')
        # "api_account_rin_desk"
        self.tested_security_account = self.data_set.get_account_by_name('account_4')
        self.tested_collateral_qty = 50
        self.current_collateral_qty = 0
        self.increased_collateral_qty = 0

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region Pre-Condition, create security Position
        self.nos_message.default_instrument_nos = self.tested_instrument
        self.nos_message.set_default_request()
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region Pre-Condition, set new InitialQty value for created position and check result
        self.security_account_position_message.find_positions(security_account_name=self.tested_security_account)
        new_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})
        try:
            security_position_fields = new_position[0].keys()
            if 'collateralQty' in security_position_fields:
                self.current_collateral_qty = new_position[0]['collateralQty']

            new_position[0].update({'initialQty': 10000})
            self.security_account_position_message.modify_security_positions(params=new_position[0])
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Response is empty new position was not created', status='FAILED', parent_id=self.test_id)

        self.wa_api_manager.send_post_request(self.security_account_position_message)

        self.security_account_position_message.find_positions(self.tested_security_account)
        modified_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})
        data_validation(self.test_id,
                        event_name="Check that initialQty equal 10000.0",
                        expected_result="10000.0",
                        actual_result=modified_position[0]['initialQty'])
        # endregion

        # region Pre-Condition, calculate Posit Qty value
        posit_qty = self.formulas_manager.calc_posit_qty(modified_position[0], self.test_id)
        print(posit_qty)
        if posit_qty > 0:
            bca.create_event(f'PositQty > 0. PositQty={posit_qty}', status='SUCCESS', parent_id=self.test_id)
        if posit_qty <= 0:
            bca.create_event(f'PositQty <= 0. PositQty={posit_qty}', status='FAILED', parent_id=self.test_id)
        # endregion

        # region step 3, Increase CollateralQty for security position
        self.security_account_position_message.create_collateral_assignments(qty=self.tested_collateral_qty)
        self.wa_api_manager.send_post_request(self.security_account_position_message)

        self.security_account_position_message.find_positions(self.tested_security_account)
        security_position_after_collateral_increase = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})
        security_position_fields_after_collateral_increase = security_position_after_collateral_increase[0].keys()
        if 'collateralQty' in security_position_fields_after_collateral_increase:
            self.increased_collateral_qty = float(security_position_after_collateral_increase[0]['collateralQty'])
            data_validation(self.test_id,
                            event_name="Check that 'CollateralQty' field was increased",
                            expected_result=float(self.current_collateral_qty) + float(self.tested_collateral_qty),
                            actual_result=self.increased_collateral_qty)
        else:
            bca.create_event('CollateralQty is not present', status='FAILED', parent_id=self.test_id)

        # region step 4, Decrease CollateralQty for security position
        self.security_account_position_message.create_collateral_assignments(qty=self.tested_collateral_qty)
        # TWI value needed for decreasing CollateralQty
        self.security_account_position_message.update_parameters({"collateralAssignmentReason": "TWI"})
        self.wa_api_manager.send_post_request(self.security_account_position_message)

        self.security_account_position_message.find_positions(self.tested_security_account)
        security_position_after_collateral_decrease = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_account_position_message),
            filter_dict={'instrID': self.tested_instrument_id})

        security_position_fields_after_collateral_decrease = security_position_after_collateral_decrease[0].keys()
        if 'collateralQty' in security_position_fields_after_collateral_decrease:
            data_validation(self.test_id,
                            event_name="Check that 'CollateralQty' field was decreased",
                            expected_result=self.increased_collateral_qty - float(
                                self.tested_collateral_qty),
                            actual_result=float(security_position_after_collateral_decrease[0]['collateralQty']))
        else:
            bca.create_event('CollateralQty is not present', status='FAILED', parent_id=self.test_id)
        # endregion