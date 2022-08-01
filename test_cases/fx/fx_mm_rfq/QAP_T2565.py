from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2565(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)

        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.qty_column = QuoteRequestBookColumns.qty.value
        self.sts_column = QuoteRequestBookColumns.status.value
        self.freenotes = "failed to get forward points through RFQ"
        self.freenotes_column = QuoteRequestBookColumns.free_notes.value
        self.rejected_sts = "Rejected"

        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol_1 = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")

        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_2w = self.data_set.get_settle_date_by_name("wk2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.settle_type_2w = self.data_set.get_settle_type_by_name("wk2")
        self.qty = random_qty(1, 3, 7)
        self.instrument = {
            "Symbol": self.symbol_1,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1

        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_qty=self.qty, leg_symbol=self.symbol_1,
                                           settle_type=self.settle_type_1w,
                                           settle_date=self.settle_date_1w, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_far_leg(leg_qty=self.qty, leg_symbol=self.symbol_1,
                                          settle_type=self.settle_type_2w,
                                          settle_date=self.settle_date_2w, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="EUR", Instrument=self.instrument)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion

        self.quote_request_book.set_filter([self.qty_column, self.qty]).check_quote_book_fields_list({
            self.sts_column: self.rejected_sts, self.freenotes_column: self.freenotes})
