import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.ApiMessageMarketQuoteRequest import ApiMessageMarketQuoteRequest


class QAP_T3190(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.nos_message = ApiMessageNewOrderSingle(data_set=self.data_set)
        self.mq_message = ApiMessageMarketQuoteRequest(data_set=data_set)
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        self.tested_fields = ['TradingPhase',
                              'StandardTradingPhase',
                              'PercentLastClosingPrice',
                              'DiffLastClosingPrice',
                              'OrdType']

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send request submitNewOrderSingle with side=Buy and receive response - Pre-Condition

        self.nos_message.set_default_request()
        self.nos_message.remove_parameter(parameter_name='SettlCurrency')
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value='10')
        self.nos_message.change_parameters_for_instrument({'InstrSymbol': self.tested_instrument['InstrSymbol'],
                                                           'SecurityID': self.tested_instrument['SecurityID'],
                                                           'SecurityExchange': self.tested_instrument[
                                                               'SecurityExchange']
                                                           }
                                                          )
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region send request submitNewOrderSingle with side=Sell and receive response - Pre-Condition
        self.nos_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        self.nos_message.change_parameter(parameter_name='Price', new_parameter_value='5')
        self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        # endregion

        # region send request - submitMarketDataRequest and receive response - step 1
        self.mq_message.tested_instrument_mq = self.tested_instrument
        self.mq_message.set_default_request()
        self.mq_message.change_key_fields_web_socket_response(
            key_fields={"MDReqID": self.mq_message.parameters['MDReqID']})
        response = self.trd_api_manager.send_http_request_and_receive_websocket_response(self.mq_message)

        market_data = self.trd_api_manager.parse_response_details_repeating_group(response)
        try:
            existing_fields = list()
            for count in range(len(market_data)):
                keys = market_data[count].keys()
                for field in self.tested_fields:
                    if field in keys:
                        bca.create_event(f'Field {field} is present', parent_id=self.test_id)
                        existing_fields.append(field)
            for field in self.tested_fields:
                if field not in existing_fields:
                    bca.create_event(f'Field {field} is not present', status='FAILED', parent_id=self.test_id)
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty, steps 1', status='FAILED', parent_id=self.test_id)
        # endregion
