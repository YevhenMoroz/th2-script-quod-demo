import time
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


class QAP_T2387(TestCase):
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
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.qty = "1000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        # TODO change venue TTL via RestAPi
        # endregion
        # region step 2
        # endregion
        self.quote_request.set_rfq_params()

        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty, Account=self.account,
                                                           Instrument=self.instrument)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        # endregion
        # region Step 3
        self.quote.set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.sleep(120)
        self.quote_cancel.set_params_for_receive(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote_cancel, key_parameters=["QuoteReqID"])
        # endregion
