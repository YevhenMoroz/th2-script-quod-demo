import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import RestApiCashAccountMessages
from test_framework.core.try_exept_decorator import try_except


class test_cash_account_counters(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_cash_account_counters_message = RestApiCashAccountMessages(data_set=data_set)
        self.api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):

        self.api_cash_account_counters_message.find_cash_account_counters(client_name='DENIS', currency='INR')
        response = self.api_manager.send_get_request_with_parameters(self.api_cash_account_counters_message)
        print(response)

