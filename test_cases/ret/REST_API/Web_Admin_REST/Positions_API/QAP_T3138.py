import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.trading_api.ApiMessageNewOrderSingle import ApiMessageNewOrderSingle
from test_framework.rest_api_wrappers.trading_api.TradingRestApiManager import TradingRestApiManager
from test_framework.rest_api_wrappers.utils.RetFormulasManager import RetFormulasManager
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Positions_API.RestApiSecurityPositionMessages import \
    RestApiSecurityPositionMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3138(TestCase):
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
        self.tested_instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')
        self.tested_collateral_qty = 100_000_000
        self.error_message = "CollateralAssignmentRequest rejected. The reason: InsufficientCollateral. Details: " \
                             "Rejected: Insufficient Collateral"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region decrease CollateralQty below to zero
        self.security_account_position_message.default_instrument_id = self.tested_instrument_id
        self.security_account_position_message.create_collateral_assignments(qty=self.tested_collateral_qty)
        # TWI value needed for decreasing CollateralQty
        self.security_account_position_message.update_parameters({"collateralAssignmentReason": "TWI"})
        collateral_assignments_response = self.wa_api_manager.parse_response_error_message_details(
            response=self.wa_api_manager.send_multiple_request(self.security_account_position_message))
        self.wa_api_manager.data_validation(test_id=self.test_id,
                                            event_name="Check that CollateralAssignmentRequest was rejected",
                                            expected_result=self.error_message,
                                            actual_result=collateral_assignments_response)
        # endregion