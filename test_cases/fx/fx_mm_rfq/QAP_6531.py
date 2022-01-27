import locale
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, QuoteStatus as qs, \
    Status
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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        gateway_side_sell = DataSet.GatewaySide.Sell
        status = DataSet.Status.Fill
        freenotes = "tomorrow is spot date, prices are indicative - manual intervention required"
        account = self.data_set.get_client_by_name("client_mm_3")
        symbol = self.data_set.get_symbol_by_name("symbol_12")
        qty1 = random_qty(1, 3, 7)
        qty2 = random_qty(1, 3, 7)
        locale.setlocale(locale.LC_ALL, 'en_US')
        qty1_test = locale.format_string("%d", int(qty1), grouping=True)
        qty2_test = locale.format_string("%d", int(qty2), grouping=True)
        security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        settle_type_tomorrow = self.data_set.get_settle_type_by_name("tomorrow")
        settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        settle_date_tom = self.data_set.get_settle_date_by_name("tomorrow")
        settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        instrument = {
            "Symbol": symbol,
            "SecurityType": security_type_swap
        }

        # Step 1
        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=symbol, leg_sec_type=security_type_fwd,
                                      settle_type=settle_type_tomorrow,
                                      settle_date=settle_date_tom, leg_qty=qty1)
        quote_request.update_far_leg(leg_symbol=symbol, leg_sec_type=security_type_fwd,
                                      settle_type=settle_type_wk1,
                                      settle_date=settle_date_wk1, leg_qty=qty1)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="USD", Instrument=instrument, OrderQty=qty1)

        self.fix_manager_gtw.send_message(quote_request)

        self.quote_request_book.set_filter(
            [qrb.qty.value, qty1_test]).check_quote_book_fields_list(
            {qrb.qty.value: qty1_test,
             qrb.free_notes.value: freenotes
             }, 'Checking that Freenotes contains correct value')

        # Step 2
        quote_request = FixMessageQuoteRequestFX().set_swap_rfq_params()
        quote_request.update_near_leg(leg_symbol=symbol, leg_sec_type=security_type_fwd,
                                      settle_type=settle_type_tomorrow,
                                      settle_date=settle_date_tom, leg_qty=qty2)
        quote_request.update_far_leg(leg_symbol=symbol, leg_sec_type=security_type_spot, settle_type=settle_type_spot,
                                     settle_date=settle_date_spo, leg_qty=qty2)
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=account,
                                                      Currency="USD", Instrument=instrument, OrderQty=qty2)
        self.fix_manager_gtw.send_message(quote_request)

        self.quote_request_book.set_filter(
            [qrb.qty.value, qty2_test]).check_quote_book_fields_list(
            {qrb.qty.value: qty2_test,
             qrb.free_notes.value: freenotes
             }, 'Checking that Freenotes contains correct value')
