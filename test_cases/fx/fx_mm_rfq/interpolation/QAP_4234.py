from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook

text = "no bid forward points for client tier `2600011' on GBP/USD WK1 on QUODFX - manual intervention required"
qty = random_qty(1, 2, 7)
qty_col = QuoteRequestBookColumns.qty.value
free_notes_col = QuoteRequestBookColumns.free_notes.value


class QAP_4234(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.quote_request_book = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        account = self.data_set.get_client_by_name("client_mm_2")
        symbol = self.data_set.get_symbol_by_name("symbol_2")
        security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        settle_date_w1 = self.data_set.get_settle_date_by_name("wk1")
        instrument = {
            "Symbol": symbol,
            "SecurityType": security_type_swap
        }
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=symbol, leg_sec_type=security_type_spot, settle_type=settle_type_spot,
                                      settle_date=settle_date_spo, leg_qty=qty)
        quote_request.update_far_leg(leg_symbol=symbol, settle_type=settle_type_wk1, leg_sec_type=security_type_fwd,
                                     settle_date=settle_date_w1, leg_qty=qty)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="GBP", Instrument=instrument)
        self.fix_manager_gtw.send_message(quote_request)

        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_request_book.set_filter([qty_col, qty]).check_quote_book_fields_list({free_notes_col: text})
