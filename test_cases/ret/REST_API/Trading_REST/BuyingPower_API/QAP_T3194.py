import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3194(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.noss_message = ApiMessageNewOrderSingleSimulate(data_set=data_set)
        self.buying_power_manager = RetFormulasManager()

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2, send submitNewOrderSimulate with side=Buy request and check Net Order Value
        self.noss_message.set_default_request()
        noss_response_buy = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        net_order_value = self.buying_power_manager.calc_net_order_value(self.test_id, noss_response_buy, side='Buy')

        data_validation(test_id=self.test_id,
                        event_name="Check Net Order Value with side=Buy",
                        expected_result=net_order_value,
                        actual_result=float(noss_response_buy['NetOrdAmt']))
        # endregion

        # region Step 3, send submitNewOrderSimulate with side=Sell request and check Net Order Value
        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='Side', new_parameter_value='Sell')
        noss_response_sell = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))

        net_order_value = self.buying_power_manager.calc_net_order_value(self.test_id, noss_response_sell,
                                                                         side='Sell')
        data_validation(test_id=self.test_id,
                        event_name="Check Net Order Value with side=Sell",
                        expected_result=net_order_value,
                        actual_result=float(noss_response_sell['NetOrdAmt']))
        # endregion
