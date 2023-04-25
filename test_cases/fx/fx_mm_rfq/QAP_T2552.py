import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import check_quote_request_id, check_quote_status
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2552(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.key_parameter = "quoterequestid"
        self.quote_state = "unavailablepricestate"
        self.quote_state_cause = "unavailablepricecause"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 2
        # endregion
        self.quote_request.set_rfq_params()
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        # endregion
        # region Step 3
        self.quote.set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.sleep(120)
        req_id = check_quote_request_id(self.quote_request)
        quote_status = check_quote_status(req_id, self.key_parameter)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check rule - Check Quote Status")
        self.verifier.compare_values("QuoteStatus", "EXP", quote_status)
        self.verifier.verify()
        # endregion
