import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import \
    RestApiCashAccountMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3353(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.cash_account_message = RestApiCashAccountMessages(data_set=data_set)
        self.cash_account_id = self.data_set.get_cash_account_counters_by_name('cash_account_counter_1')
        self.error_message = "Request fails: TransferAmt inserted must be positive"
        self.cash_transfer_types = self.data_set.get_cash_transfer_types_by_name('cash_transfer_types_1')

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region, send Cash Account Transfer with negative value and different Transaction Types
        for key, value in self.cash_transfer_types.items():
            self.cash_account_message.modify_cash_account_transfer(cash_account_id=self.cash_account_id,
                                                                   transfer_type=self.cash_transfer_types[key],
                                                                   transfer_amount=-10)
            error_response = self.wa_api_manager.parse_response_error_message_details(
                response=self.wa_api_manager.send_multiple_request(self.cash_account_message))
            data_validation(self.test_id,
                            event_name="Cash Transfer with negative value and "
                                                                         f"transfer type '{value}'",
                            expected_result=self.error_message,
                            actual_result=error_response)
        # endregion
