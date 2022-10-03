import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3139(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.security_account_position_message = RestApiSecurityPositionMessages(data_set=data_set)
        # TCS-IQ[NSE]
        self.tested_instrument = self.data_set.get_trading_api_instrument_by_name("instrument_2")
        # ePKRr68Nr7pDFdVkx6amaQ
        self.tested_collateral_qty = 100_000_000
        self.error_message = "CollateralAssignmentRequest rejected. The reason: ExcessiveSubstitution. Details: " \
                             "Rejected: Excessive Substitution"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region increase CollateralQty greater than PositQty
        self.security_account_position_message.create_collateral_assignments(qty=self.tested_collateral_qty)
        collateral_assignments_response = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.security_account_position_message))
        data_validation(test_id=self.test_id,
                        event_name="Check that CollateralAssignmentRequest was rejected",
                        expected_result=self.error_message,
                        actual_result=collateral_assignments_response)
        # endregion
