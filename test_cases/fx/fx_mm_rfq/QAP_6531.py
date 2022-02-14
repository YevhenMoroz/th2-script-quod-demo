from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_6531(TestCase):

    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)

        self.freenotes = "tomorrow is spot date, prices are indicative - manual intervention required"
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_12")
        self.qty1 = random_qty(1, 3, 7)
        self.qty2 = random_qty(1, 3, 7)
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.settle_type_tomorrow = self.data_set.get_settle_type_by_name("tomorrow")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_tom = self.data_set.get_settle_date_by_name("tomorrow")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):


        # Step 1
        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_fwd,
                                      settle_type=self.settle_type_tomorrow,
                                      settle_date=self.settle_date_tom, leg_qty=self.qty1)
        quote_request.update_far_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_fwd,
                                     settle_type=self.settle_type_wk1,
                                     settle_date=self.settle_date_wk1, leg_qty=self.qty1)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency="USD", Instrument=self.instrument, OrderQty=self.qty1)

        self.fix_manager_gtw.send_message(quote_request)

        self.quote_request_book.set_filter(
            [qrb.qty.value, self.qty1]).check_quote_book_fields_list(
            {qrb.free_notes.value: self.freenotes})

        # Step 2
        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_fwd,
                                      settle_type=self.settle_type_tomorrow,
                                      settle_date=self.settle_date_tom, leg_qty=self.qty2)
        quote_request.update_far_leg(leg_symbol=self.symbol, leg_sec_type=self.security_type_spot, settle_type=self.settle_type_spot,
                                     settle_date=self.settle_date_spo, leg_qty=self.qty2)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency="USD", Instrument=self.instrument, OrderQty=self.qty2)
        self.fix_manager_gtw.send_message(quote_request)

        self.quote_request_book.set_filter(
            [qrb.qty.value, self.qty2]).check_quote_book_fields_list(
            {qrb.free_notes.value: self.freenotes})
