import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageMarketDataRequest import ApiMessageMarketDataRequest


class QAP_T3611(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.case_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.md_message = ApiMessageMarketDataRequest(data_set=self.data_set)
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_1")

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send request submitNewOrderSingle and receive response - step 1

        self.nos_message.set_default_request()
        self.nos_message.change_parameters_for_instrument({'InstrSymbol': self.tested_instrument['InstrSymbol'],
                                                           'SecurityID': self.tested_instrument['SecurityID'],
                                                           'SecurityExchange': self.tested_instrument[
                                                               'SecurityExchange']
                                                           }
                                                          )
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region send request - submitMarketDataRequest and receive response - step 2
        self.md_message.set_default_request()
        self.md_message.change_key_fields_web_socket_response(
            key_fields={"MDReqID": self.md_message.parameters['MDReqID']})
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.md_message)
        # endregion
