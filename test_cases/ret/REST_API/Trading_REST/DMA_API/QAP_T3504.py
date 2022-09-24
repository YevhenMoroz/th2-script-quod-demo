import os
from datetime import timedelta, datetime

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3504(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.time_now = datetime.utcnow()

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region send request submitNewOrderSingle and receive response - step 1
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='ExpireDate',
                                          new_parameter_value=(self.time_now + timedelta(days=2)).strftime("%Y%m%d"))
        self.nos_message.change_parameter(parameter_name='TimeInForce', new_parameter_value='GoodTillDate')
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Open'})

        response = self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        parsed_response = self.trd_api_manager.parse_response_details(response)
        try:
            data_validation(test_id=self.test_id,
                            event_name="Check TimeInForce value",
                            expected_result="GoodTillDate",
                            actual_result=parsed_response['TimeInForce'])
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion
