import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderModificationRequest import ApiMessageOrderModification
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T8250(TestCase):
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
        self.formulas_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=data_set)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.modification_message = ApiMessageOrderModification(data_set=data_set)
        self.security_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        # "api_client_gross"
        self.client = self.data_set.get_client_by_name('client_6')
        # "api_account_gross"
        self.security_account = self.data_set.get_account_by_name('account_6')
        # "api_cash_account_gross_INR"
        self.cash_account = self.data_set.get_cash_account_by_name('cash_account_3')
        # "ePKRr68Nr7pDFdVkx6amaQ"
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')
        self.message_type_modification_reject = TradingRestApiMessageType.OrderModificationReject.value
        self.error_message = '11604 Insufficient holdings: Selling Power (-40) negative'

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-Condition, create new order with side=Buy
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='ClientAccountGroupID', new_parameter_value=self.client)
        self.nos_message.change_parameter(parameter_name='ClientCashAccountID', new_parameter_value=self.cash_account)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocClientAccountID': self.security_account})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region Pre-Condition, create new order with side=Sell
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.nos_message.change_parameter(parameter_name='ClientAccountGroupID', new_parameter_value=self.client)
        self.nos_message.change_parameter(parameter_name='ClientCashAccountID', new_parameter_value=self.cash_account)
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=3)
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=10)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations', fields={'AllocQty': 10})
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocClientAccountID': self.security_account})
        self.nos_message.change_key_fields_web_socket_response({})

        nos_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message))
        print(nos_response)
        # endregion

        # region Pre-Condition, set new InitialQty value for created position and check result
        self.security_position_message.find_positions(security_account_name=self.security_account)
        new_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
            filter_dict={'instrID': self.instrument_id})

        try:
            new_position[0].update({'initialQty': 100})
            new_position[0].update({'cumBuyQty': 0})
            new_position[0].update({'cumSellQty': 0})
            new_position[0].update({'transferredInQty': 0})
            new_position[0].update({'transferredOutQty': 0})
            new_position[0].update({'exercisedQty': 0})
            new_position[0].update({'leavesBuyQty': 0})
            new_position[0].update({'leavesSellQty': 0})
            new_position[0].update({'reservedQty': 0})
            self.security_position_message.modify_security_positions(params=new_position[0])
        except(KeyError, TypeError, IndexError):
            bca.create_event("Initial Qty isn't present in the new position", status="FAILED", parent_id=self.test_id)

        self.wa_api_manager.send_post_request(self.security_position_message)

        self.security_position_message.find_positions(self.security_account)
        modified_position = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
            filter_dict={'instrID': self.instrument_id})
        try:
            data_validation(test_id=self.test_id,
                            event_name="Check that initialQty equal 100.0",
                            expected_result="100.0",
                            actual_result=modified_position[0]['initialQty'])
        except(KeyError, TypeError, IndexError):
            bca.create_event("Initial Qty isn't present in the modified position", status="FAILED", parent_id=self.test_id)
        # endregion

        # region Check Position Qty
        total_posit_qty = self.formulas_manager.calc_posit_qty(self.test_id, modified_position[0])
        if int(total_posit_qty) > 0:
            bca.create_event(f'Position Qty > 0', status='SUCCESS', parent_id=self.test_id)
        elif int(total_posit_qty) <= 0:
            bca.create_event(f'Position Qty <= 0', status='FAILED', parent_id=self.test_id)
        # endregion

        # region send request submitOrderModificationRequest with values which greater than Position Qty
        if 'BuyingPowerLimitAmt' in nos_response.keys():
            modification_params = {'OrdQty': 150, 'Side': 'Sell'}
            self.modification_message.set_modification_parameters(nos_response,
                                                                  modification_params,
                                                                  negative_case=True)
            self.modification_message.change_key_fields_web_socket_response(
                {'_type': self.message_type_modification_reject})

            parsed_modification_response = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_websocket_response(
                    self.modification_message))
            if 'FreeNotes' in parsed_modification_response.keys():
                data_validation(test_id=self.test_id,
                                event_name='Check that Insufficient holdings: Selling Power',
                                expected_result=self.error_message,
                                actual_result=parsed_modification_response['FreeNotes'])
            else:
                bca.create_event(f"Error message isn't present in the modification response", status="FAILED",
                                 parent_id=self.test_id)
        else:
            bca.create_event(f"BuyingPowerLimitAmt isn't present in the NOS response", status="FAILED",
                             parent_id=self.test_id)

        # endregion
