from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class QAP_T2392(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_ndf_1")
        self.currency = self.data_set.get_currency_by_name('currency_usd')
        self.security_type_ndf = self.data_set.get_security_type_by_name("fx_ndf")
        self.security_type_nds = self.data_set.get_security_type_by_name("fx_nds")
        self.settle_date_spo_ndf = self.data_set.get_settle_date_by_name("spo_ndf")
        self.settle_date_wk1_ndf = self.data_set.get_settle_date_by_name("wk1_ndf")
        self.qty = "1000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_nds
        }
        self.text = "11609 'InstrType': NDS error: 'OrdQty' present"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 2
        self.quote_request.set_swap_rfq_params()

        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Instrument=self.instrument, Currency=self.currency,
                                                           OrderQty=self.qty)
        self.quote_request.update_near_leg(leg_symbol=self.symbol, settle_date=self.settle_date_spo_ndf,
                                           leg_qty=self.qty)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_ndf,
                                          settle_date=self.settle_date_wk1_ndf, leg_qty=self.qty)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 3
        self.quote_reject.set_quote_reject_swap(self.quote_request, text=self.text)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(self.quote_reject)
        # endregion
