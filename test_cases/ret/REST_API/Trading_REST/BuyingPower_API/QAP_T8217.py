import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderModificationRequest import ApiMessageOrderModification
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import \
    RestApiCashAccountMessages
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.utils.booked_amount_verifier import booked_amount_validation


class QAP_T8217(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.web_admin = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.web_admin)
        self.formulas_manager = RetFormulasManager()
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.modification_message = ApiMessageOrderModification(data_set=data_set)
        self.cash_account_message = RestApiCashAccountMessages(data_set=self.data_set)
        self.security_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        self.cash_account_id = self.data_set.get_cash_account_counters_by_name('cash_account_counter_1')
        self.security_account = self.data_set.get_account_by_name('account_4')
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')
        self.fee = self.data_set.get_fee_by_name('fees_1')
        self.commission = self.data_set.get_commission_by_name('commission_1')
        self.qty = 3
        self.price = 4

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region check BuyingPower updating upon order modification, Buy side
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=self.price)
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=self.qty)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocQty': self.qty})
        self.nos_message.change_key_fields_web_socket_response({})

        response = self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        nos_response = self.trd_api_manager.parse_response_details(response=response)

        if 'ExecType' in nos_response.keys() and nos_response['ExecType'] == 'Open':
            initial_net_order_value = float(nos_response['NetOrdAmt'])
            self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)
            booked_amount_after_order_creation = self.wa_api_manager.parse_response_details(
                response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))
            self.security_position_message.find_positions(security_account_name=self.security_account)

            position_after_order_creation = self.wa_api_manager.parse_response_details(
                response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
                filter_dict={'instrID': self.instrument_id})

            self.qty += 5
            self.modification_message.set_modification_parameters(nos_response, {'OrdQty': self.qty})
            self.modification_message.change_key_fields_web_socket_response({'ExecType': 'Replaced'})
            modified_response = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_websocket_response(
                    self.modification_message))

            if 'ExecType' in modified_response.keys() and modified_response['ExecType'] == 'Replaced':
                execution_type_order_modified = modified_response['ExecType']

                self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)
                booked_amount_after_modification_increase = self.wa_api_manager.parse_response_details(
                    response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))

                self.security_position_message.find_positions(security_account_name=self.security_account)
                position_after_modification_increase = self.wa_api_manager.parse_response_details(
                    response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
                    filter_dict={'instrID': self.instrument_id})

                amended_net_order_value = self.qty * self.price + self.commission + self.fee
                calculation_results_after_order_modification = self.formulas_manager.calc_booked_amount_buy_side(
                    test_id=self.test_id,
                    response_wa_cash_account=booked_amount_after_order_creation[0],
                    response_wa_security_account=position_after_order_creation,
                    initial_net_order_value=initial_net_order_value,
                    execution_type=execution_type_order_modified,
                    amended_net_order_value=amended_net_order_value)
                booked_amount_validation(test_id=self.test_id,
                                         event_name='Booked Amount calculation upon order Modification. Side=Buy.'
                                                    f'(Increase Qty to {self.qty})',
                                         booked_amount_current=booked_amount_after_modification_increase[0],
                                         booked_amount_simulated=calculation_results_after_order_modification,
                                         reserved_qty_current=position_after_modification_increase[0])

                self.qty -= 5
                self.modification_message.set_modification_parameters(nos_response, {'OrdQty': self.qty})
                self.modification_message.change_key_fields_web_socket_response({'ExecType': 'Replaced'})
                modified_response = self.trd_api_manager.parse_response_details(
                    response=self.trd_api_manager.send_http_request_and_receive_websocket_response(
                        self.modification_message))

                if 'ExecType' in modified_response.keys() and modified_response['ExecType'] == 'Replaced':
                    self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)
                    booked_amount_after_modification_decrease = self.wa_api_manager.parse_response_details(
                        response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))

                    self.security_position_message.find_positions(security_account_name=self.security_account)
                    position_after_modification_decrease = self.wa_api_manager.parse_response_details(
                        response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
                        filter_dict={'instrID': self.instrument_id})

                    calculation_results_after_order_modification = self.formulas_manager.calc_booked_amount_buy_side(
                        test_id=self.test_id,
                        response_wa_cash_account=booked_amount_after_modification_increase[0],
                        response_wa_security_account=position_after_modification_increase,
                        initial_net_order_value=amended_net_order_value,
                        execution_type=execution_type_order_modified,
                        amended_net_order_value=self.qty * self.price + self.commission + self.fee)
                    booked_amount_validation(test_id=self.test_id,
                                             event_name='Booked Amount calculation upon order Modification. Side=Buy'
                                                        f'(Decrease Qty to {self.qty})',
                                             booked_amount_current=booked_amount_after_modification_decrease[0],
                                             booked_amount_simulated=calculation_results_after_order_modification,
                                             reserved_qty_current=position_after_modification_decrease[0])
                else:
                    bca.create_event(f"Modification response wasn't received, (decrease Qty to {self.qty})",
                                     status="FAILED",
                                     parent_id=self.test_id)
            else:
                bca.create_event(f"Modification response wasn't received, (increase Qty to {self.qty})",
                                 status="FAILED",
                                 parent_id=self.test_id)
        else:
            bca.create_event("New Order Single response wasn't received", status="FAILED", parent_id=self.test_id)
        # endregion




