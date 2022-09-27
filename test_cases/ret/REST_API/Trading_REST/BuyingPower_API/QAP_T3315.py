import os
from datetime import timedelta, datetime

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderModificationRequest import ApiMessageOrderModification


class QAP_T3315(TestCase):
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

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region step 1, create new order, Side=Buy
        self.nos_message.set_default_request()
        self.nos_message.change_key_fields_web_socket_response({})
        nos_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        )
        # endregion

        # region step 2, Do amend for new order and check results
        if 'BuyingPowerLimitAmt' in nos_response.keys():
            self.noss_message.set_default_request()
            noss_response_before_modification = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message)
            )
            time_now = datetime.utcnow()
            expire_date_value = (time_now + timedelta(days=2)).strftime("%Y%m%d")
            self.modification_message.set_modification_parameters(nos_response,
                                                                  {'TimeInForce': 'GoodTillDate',
                                                                   'ExpireDate': expire_date_value})
            self.modification_message.change_key_fields_web_socket_response({'ExecType': 'Replaced'})
            modification_response = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_websocket_response(
                    self.modification_message))
            data_validation(test_id=self.test_id,
                            event_name='Check that TIF was changed',
                            expected_result='GoodTillDate',
                            actual_result=modification_response['TimeInForce'])
            self.noss_message.set_default_request()
            noss_response_after_modification = self.trd_api_manager.parse_response_details(
                response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message)
            )
            if 'BuyingPowerLimitAmt' in noss_response_after_modification.keys():
                data_validation(test_id=self.test_id,
                                event_name='Check that Buying Power value was not changed after modification request.',
                                expected_result=noss_response_before_modification['BuyingPowerLimitAmt'],
                                actual_result=noss_response_after_modification['BuyingPowerLimitAmt'])
            else:
                bca.create_event(f"BuyingPowerLimitAmt isn't present in the NOSS response", status="FAILED",
                                 parent_id=self.test_id)
        else:
            bca.create_event(f"BuyingPowerLimitAmt isn't present in the NOS response", status="FAILED",
                             parent_id=self.test_id)
        # endregion



