from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteResponseFX import FixMessageQuoteResponseFX


class QAP_T2629(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.dc_fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.quote_response = FixMessageQuoteResponseFX()
        self.quote_cancel = FixMessageQuoteCancelFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params()
        response = self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        self.sleep(1)
        # endregion

        # region Step 2
        self.quote_response.set_params_for_quote_response(response[0], self.quote_request)
        self.fix_manager_sel.send_message(self.quote_response)
        # endregion
        # region Step 3
        self.quote_cancel.set_params_for_receive(self.quote_request)
        self.dc_fix_verifier.check_fix_message(self.quote_cancel)
