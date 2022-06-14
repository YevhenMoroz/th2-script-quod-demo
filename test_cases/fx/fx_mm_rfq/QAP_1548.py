import time
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
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, Status as st
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_1548(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.qty = "55000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params()

        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty, Account=self.account,
                                                           Instrument=self.instrument, Currency=self.currency)
        self.fix_manager_sel.send_message(self.quote_request)

        self.dealer_intervention.set_list_filter(["Qty", self.qty])
        self.dealer_intervention.assign_quote(row_number=1)

        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        # endregion
        # region Step 2
        self.dealer_intervention.reject_quote()
        self.dealer_intervention.close_window()
        # endregion
        # region Step 3
        self.quote_request_book.set_filter(
            [qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.status.value: st.rejected.value}, 'Checking quote request status')
        # endregion
