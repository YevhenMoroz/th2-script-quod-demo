import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageVenueListRequest import ApiMessageVenueListRequest


class QAP_T3500(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     case_id=self.test_id)
        self.venue_list_message = ApiMessageVenueListRequest(data_set=data_set)
        self.tested_fields = ['TradingPhase', 'TradingSession', 'OrdType', 'SupportDisplayQty', 'TimeInForce']
        self.tested_venue = 'National Stock Exchange'

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send request submitVenueListRequest and receive response - step 1
        self.venue_list_message.change_key_fields_http_response({'ReplyType': 'Accepted'})
        response = self.trd_api_manager.send_http_request_and_receive_http_response(self.venue_list_message)
        venues = self.trd_api_manager.parse_response_details_repeating_group(response)
        try:
            for count in range(len(venues)):
                if venues[count].get('VenueName') == self.tested_venue:
                    keys = venues[count].keys()
                    for field in self.tested_fields:
                        if field in keys:
                            bca.create_event(f'Field {field} is present', parent_id=self.test_id)
                        else:
                            bca.create_event(f'Field {field} is not present', parent_id=self.test_id, status='FAILED')
        except (KeyError, TypeError):
            bca.create_event(f'Response is empty, steps 1', status='FAILED', parent_id=self.test_id)
        # endregion
