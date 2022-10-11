import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderModificationRequest import ApiMessageOrderModification
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T8248(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=data_set)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.modification_message = ApiMessageOrderModification(data_set=data_set)
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        self.error_message = '11628 Insufficient Buying Power'
        self.message_type_modification_reject = TradingRestApiMessageType.OrderModificationReject.value
        self.message_type_execution_report = TradingRestApiMessageType.ExecutionReport.value
        self.price = 4
        self.qty = 4

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send requests submitNewOrderSingle and  trade order with status: PartiallyFilled
        self.nos_message.set_default_request()

        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=self.price)
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=self.qty)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocQty': self.qty})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)

        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Buy')
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value=self.price * 2)
        self.nos_message.change_parameter(parameter_name='OrdQty', new_parameter_value=self.qty * 2)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocQty': self.qty * 2})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})
        nos_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message))

        self.modification_message.set_modification_parameters(nos_response,
                                                              {'Price': self.price * 1000000},
                                                              negative_case=True)
        self.modification_message.change_key_fields_web_socket_response(
            {'_type': self.message_type_modification_reject})

        parsed_modification_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(
                self.modification_message))
        if 'FreeNotes' in parsed_modification_response.keys():
            data_validation(test_id=self.test_id,
                            event_name='Check that Insufficient Buying Power If Modified Order Value greater than existing BuyingPower',
                            expected_result=self.error_message,
                            actual_result=parsed_modification_response['FreeNotes'].split('.')[0])
        # endregion
