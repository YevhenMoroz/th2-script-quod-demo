import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T8246(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.error_message = '11901 Not sufficient Buying Power'

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send requests submitNewOrderSingleSimulate and receive BuyingPower value
        self.noss_message.set_default_request()
        response = self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message)
        noss_response = self.trd_api_manager.parse_response_details(response=response)
        if 'BuyingPowerLimitAmt' in noss_response.keys():

            self.noss_message.change_parameter(parameter_name='Price',
                                               new_parameter_value=float(noss_response['BuyingPowerLimitAmt']) + 10)
            self.noss_message.change_key_fields_http_response({'ReplyType': 'Rejected'})
            new_noss_response = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
            if 'ErrorMessage' in new_noss_response.keys():
                data_validation(test_id=self.test_id,
                                event_name='Check that Not sufficient Buying Power if Order is greater than existing BuyingPower',
                                expected_result=self.error_message,
                                actual_result=new_noss_response['ErrorMessage'])
        else:
            bca.create_event(f"BuyingPowerLimitAmt isn't present in response", status='FAILED', parent_id=self.test_id)
        # endregion
