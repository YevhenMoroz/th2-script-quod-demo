import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderModificationRequest import ApiMessageOrderModification
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3606(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_2")

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region send NewOrderSingle and check result - step 1
        self.nos_message.set_default_request()
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})

        response = self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        parsed_response = self.trd_api_manager.parse_response_details(response)

        try:
            data_validation(test_id=self.test_id,
                            event_name="Check PosValidity field",
                            expected_result="Delivery",
                            actual_result=parsed_response["PosValidity"])
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion

        # region send ModificationRequest and check result - step 1
        modification_parameters = {
            'ClOrdID': parsed_response['ClOrdID'],
            'Side': parsed_response['Side'],
            'OrdType': parsed_response['OrdType'],
            'ClientAccountGroupID': parsed_response['ClientAccountGroupID'],
            'OrdQty': parsed_response['OrdQty'],
            'Instrument': self.tested_instrument,
            'Price': parsed_response['Price'],
            'SettlCurrency': parsed_response['SettlCurrency'],
            'PosValidity': 'TP2'
        }
        modification_message = ApiMessageOrderModification(parameters=modification_parameters, data_set=self.data_set)
        modification_response = self.trd_api_manager.send_http_request_and_receive_websocket_response(
            modification_message)
        parsed_modification_response = self.trd_api_manager.parse_response_details(modification_response)

        try:
            data_validation(test_id=self.test_id,
                            event_name="Check PosValidity field after sending Modification request",
                            expected_result="TPlus2",
                            actual_result=parsed_modification_response["PosValidity"])
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=self.test_id)
