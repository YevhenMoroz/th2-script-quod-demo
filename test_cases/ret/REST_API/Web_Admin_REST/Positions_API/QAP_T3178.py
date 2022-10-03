import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiCashAccountMessages import RestApiCashAccountMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3178(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.cash_account_messages = RestApiCashAccountMessages(data_set=data_set)
        # "api_account_rin_desk"
        self.tested_security_account = self.data_set.get_account_by_name('account_4')
        self.error_message = "Request fails: code=QUOD-32533:Request not allowed:  The " \
                             f"ClientCashAccountID={self.tested_security_account} match a SecurityAccount.ClientAccountID"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create Cash Account with non-unique ClientCashAccountID
        self.cash_account_messages.create_cash_account(self.tested_security_account, "INR", self.tested_security_account)
        parsed_response = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.cash_account_messages))
        data_validation(test_id=self.test_id,
                        event_name="Check that new CashAccount was not created",
                        expected_result=self.error_message,
                        actual_result=parsed_response)
        # endregion
