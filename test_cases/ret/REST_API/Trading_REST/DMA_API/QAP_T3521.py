import os

from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle


class QAP_T3521(TestCase):
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
        self.tested_client = self.data_set.get_client_by_name("client_5")
        self.tested_account = self.data_set.get_account_by_name("account_5")
        self.tested_free_notes = f" cannot use account group &apos {self.tested_client}&apos"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send new order and verify result - step 1
        self.nos_message.set_default_request()
        self.nos_message.change_parameter(parameter_name='ClientAccountGroupID', new_parameter_value=self.tested_client)
        self.nos_message.change_parameter_in_component(component_name='PreTradeAllocations',
                                                       fields={'AllocClientAccountID': self.tested_account})
        self.nos_message.change_key_fields_web_socket_response({'OrderStatus': 'Rejected'})

        response = self.trd_api_manager.send_http_request_and_receive_websocket_response(self.nos_message)
        parsed_response = self.trd_api_manager.parse_response_details(response)
        free_notes = parsed_response['FreeNotes'].split(';')[2:4]

        verifier(case_id=self.test_id,
                 event_name="Check FreeNotes content",
                 expected_value=self.tested_free_notes,
                 actual_value=" ".join(free_notes))
        # endregion
