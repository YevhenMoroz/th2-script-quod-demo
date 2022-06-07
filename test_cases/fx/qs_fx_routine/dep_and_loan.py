from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum, Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class DepAndLoan(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.order = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.status = Status.Fill

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_deposit_and_loan_param()
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 2
        self.quote.set_params_for_deposit_and_loan(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        self.order.set_default_deposit_and_loan(self.quote_request, response[0])
        self.fix_manager_sel.send_message_and_receive_response(self.order, self.test_id)

        self.execution_report.set_params_from_deposit_and_loan(self.order, self.status)
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion
