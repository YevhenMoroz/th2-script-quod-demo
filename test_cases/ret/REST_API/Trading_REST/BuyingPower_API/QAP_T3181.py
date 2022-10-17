import os

from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingleSimulate import \
    ApiMessageNewOrderSingleSimulate


class QAP_T3181(TestCase):
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
        self.tested_free_notes = "11901 Not sufficient Buying Power"
        self.tested_qty = 1_000_000_000

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step , send submitNewOrderSimulate request and check that FreeNotes with error message
        self.noss_message.set_default_request()
        self.noss_message.change_parameter(parameter_name='OrdQty', new_parameter_value=self.tested_qty)
        self.noss_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                        fields={'AllocQty': self.tested_qty})
        self.noss_message.change_key_fields_web_socket_response({'OrderStatus': 'Rejected'})
        noss_response = self.trd_api_manager.parse_response_details(
            response=self.trd_api_manager.send_http_request_and_receive_http_response(self.noss_message))
        print(noss_response)
        data_validation(test_id=self.test_id,
                        event_name="Check FreeNotes field with an error message",
                        expected_result=self.tested_free_notes,
                        actual_result=noss_response['ErrorMessage'])
        # endregion
