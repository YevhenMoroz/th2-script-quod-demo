from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class QAP_T2482(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.quote = FixMessageQuoteFX()
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.qty = str(random_qty(from_number=1, to_number=9, len=6))
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.text = "11505 Runtime error (cannot process request without client)"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params()
        self.quote_request.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account"])
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty, Instrument=self.instrument)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 2
        self.quote_reject.set_quote_reject_params(self.quote_request, text=self.text)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(fix_message=self.quote_reject, key_parameters=["QuoteReqID"])
        # endregion
