import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns as qrb, \
    QuoteBookColumns as qb, QuoteStatus as qs


class QAP_T2978(TestCase):
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
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.qty = str(random_qty(from_number=1, to_number=9, len=6))
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
                                                           Instrument=self.instrument)
        response = self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 2
        self.quote_cancel.set_params_for_cancel(self.quote_request, response[0])
        self.fix_manager_sel.send_message(self.quote_cancel)
        # endregion
        # region Step 3
        self.quote_request_book.set_filter(
            [qrb.instrument_symbol.value, self.symbol, qrb.qty.value, self.qty]).check_quote_book_fields_list(
            {qrb.instrument_symbol.value: self.symbol,
             qrb.quote_status.value: qs.canceled.value,
             qrb.status.value: qs.terminated.value}, 'Checking that regular currency RFQ is placed')
        # endregion
        # region Step 4
        self.quote_book.set_filter(
            [qb.security_id.value, self.symbol, qb.ord_qty.value, self.qty]).check_quote_book_fields_list(
            {qb.security_id.value: self.symbol,
             qb.quote_status.value: qs.canceled.value,
             qb.ord_qty.value: f'{self.qty[:3]},{self.qty[3:]}'}, 'Checking currency value in quote book')
        # endregion
