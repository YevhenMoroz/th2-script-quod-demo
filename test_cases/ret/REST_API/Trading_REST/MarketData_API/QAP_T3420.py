import os

from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.trading_api.ApiMessageHistoricalMarketDataRequest import \
    ApiMessageHistoricalMarketDataRequest
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3420(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.http = self.environment.get_list_trading_rest_api_environment()[0].session_alias_http
        self.trd_api_manager = TradingRestApiManager(session_alias_http=self.http,
                                                     case_id=self.test_id)
        self.historical_md = ApiMessageHistoricalMarketDataRequest(data_set=data_set)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region send request submitHistoricalMarketDataRequest and receive response - step 1
        self.historical_md.set_default_request()
        self.historical_md.change_key_fields_http_response({'ReplyType': 'Accepted'})

        response = self.trd_api_manager.send_http_request_and_receive_http_response(self.historical_md)
        parsed_response = self.trd_api_manager.parse_response_details(response)
        try:
            data_validation(test_id=self.test_id,
                            event_name="Check MDEntryPx field",
                            expected_result="3333.0",
                            actual_result=parsed_response["MDEntryPx"])
            data_validation(test_id=self.test_id,
                            event_name="Check MDEntryDateTime field",
                            expected_result="2022-01-27T11:07:59",
                            actual_result=parsed_response["MDEntryDateTime"])
        except:
            bca.create_event(f'Fail test event. Response is empty',
                             status='FAILED',
                             parent_id=self.test_id)
        # endregion
