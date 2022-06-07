import os

from datetimerange import DateTimeRange
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageOrderArchiveMassStatusRequest import \
    ApiMessageOrderArchiveMassStatusRequest


class QAP_6401(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.web_socket = self.environment.get_list_trading_rest_api_environment()[0].session_alias_web_socket
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     session_alias_web_socket=self.web_socket,
                                                     case_id=self.test_id)
        self.order_archive = ApiMessageOrderArchiveMassStatusRequest(data_set=data_set)

        self.start_date_time = "2022-04-28T00:00:00"
        self.end_date_time = "2022-04-29T23:59:59"
        self.time_range = DateTimeRange(self.start_date_time, self.end_date_time)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        # region send submitOrderArchiveMassStatusRequest and check result - step 1
        self.order_archive.set_default_request()
        self.order_archive.change_key_fields_http_response({'ReplyType': 'Accepted'})
        response = self.trd_api_manager.send_http_request_and_receive_http_response(self.order_archive)
        parsed_response = self.trd_api_manager.parse_response_details_repeating_group(response)
        for order in range(len(parsed_response)):
            transact_time = parsed_response[order].get('TransactTime')
            if transact_time is not None and transact_time in self.time_range:
                bca.create_event(f'TransactTime {transact_time} included in the time period {self.time_range}',
                                 parent_id=self.test_id)
            if transact_time is not None and transact_time not in self.time_range:
                bca.create_event(f'TransactTime {transact_time} is wrong',
                                 status='FAILED',
                                 parent_id=self.test_id)

        # endregion
