import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderCancelRequest import ApiMessageOrderCancel
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import \
    RestApiCashAccountMessages
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.utils.booked_amount_verifier import booked_amount_validation


class QAP_T8214(TestCase):
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
        self.cancel_message = ApiMessageOrderCancel(data_set=data_set)
        self.cash_account_message = RestApiCashAccountMessages(data_set=self.data_set)
        self.security_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        self.cash_account_id = self.data_set.get_cash_account_counters_by_name('cash_account_counter_1')
        self.security_account = self.data_set.get_account_by_name('account_4')
        self.instrument = self.data_set.get_trading_api_instrument_by_name('instrument_4')
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_4')
        self.fee = self.data_set.get_fee_by_name('fees_1')
        self.commission = self.data_set.get_commission_by_name('commission_1')
        self.qty = 4
        self.price = 8

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region, Get current Cash Components and Security Positions, pre-condition
        self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)
        booked_amount_before_order_creation = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))
        self.security_position_message.find_positions(security_account_name=self.security_account)
        position_before_order_creation = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
            filter_dict={'instrID': self.instrument_id})
        # endregion

        # region check BuyingPower updating upon order creation, Buy side
        self.nos_message.default_instrument_nos = self.instrument
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=self.price)
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=self.qty)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocQty': self.qty})
        self.nos_message.change_key_fields_web_socket_response({})

        nos_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message))

        if 'ExecType' in nos_response.keys() and nos_response['ExecType'] == 'Open':
            initial_net_order_value = float(nos_response['NetOrdAmt'])
            self.cash_account_message.find_cash_account_counters(cash_account_id=self.cash_account_id)

            booked_amount_after_buy_order_creation = self.wa_api_manager.parse_response_details(
                response=self.wa_api_manager.send_get_request_with_parameters(self.cash_account_message))
            self.security_position_message.find_positions(security_account_name=self.security_account)

            position_after_buy_order_creation = self.wa_api_manager.parse_response_details(
                response=self.wa_api_manager.send_get_request_with_parameters(self.security_position_message),
                filter_dict={'instrID': self.instrument_id})

            calculation_results_buy_side = self.formulas_manager.calc_booked_amount_buy_side(
                test_id=self.test_id,
                response_wa_cash_account=
                booked_amount_before_order_creation[0],
                response_wa_security_account=
                position_before_order_creation,
                initial_net_order_value=initial_net_order_value,
                execution_type=nos_response['ExecType'])

            booked_amount_validation(test_id=self.test_id,
                                     event_name='Booked Amount calculation upon order Creation. Side=Buy',
                                     booked_amount_current=booked_amount_after_buy_order_creation[0],
                                     booked_amount_simulated=calculation_results_buy_side,
                                     reserved_qty_current=position_after_buy_order_creation[0])

            # region Cancel new order and check BuyingPower updating, Side=Buy
            self.cancel_message.set_cancellation_parameters(nos_response)
            self.cancel_message.change_key_fields_web_socket_response({'OrderStatus': 'Cancelled'})
            cancel_response_buy_side = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.cancel_message))

            if 'ExecType' in cancel_response_buy_side.keys():

                calculation_results_after_buy_order_cancellation = self.formulas_manager.calc_booked_amount_buy_side(
                    test_id=self.test_id,
                    response_wa_cash_account=booked_amount_after_buy_order_creation[0],
                    response_wa_security_account=position_after_buy_order_creation,
                    initial_net_order_value=initial_net_order_value,
                    execution_type=cancel_response_buy_side['ExecType']
                )

                booked_amount_validation(test_id=self.test_id,
                                         event_name='Booked Amount calculation upon order Cancellation. Side=Buy',
                                         booked_amount_current=booked_amount_before_order_creation[0],
                                         booked_amount_simulated=calculation_results_after_buy_order_cancellation,
                                         reserved_qty_current=position_before_order_creation[0])
            else:
                bca.create_event("Order Cancel response wasn't received. (Side=Buy)",
                                 status="FAILED", parent_id=self.test_id)
            # endregion
        else:
            bca.create_event("New Order Single response wasn't received. (Side=Buy)",
                             status="FAILED", parent_id=self.test_id)
        # endregion


