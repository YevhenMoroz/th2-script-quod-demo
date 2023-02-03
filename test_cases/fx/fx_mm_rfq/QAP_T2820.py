from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets import constants
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns, QuoteStatus, Status
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2820(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument_spot = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.instrument_fwd = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.qty = random_qty(1, 2, 7)
        self.cur_column = QuoteRequestBookColumns.currency.value
        self.qty_column = QuoteRequestBookColumns.qty.value
        self.sts_column = QuoteRequestBookColumns.status.value
        self.quote_status_column = QuoteRequestBookColumns.quote_status.value
        self.sts_new = Status.new.value
        self.sts_accepted = QuoteStatus.accepted.value
        self.sts_filled = QuoteStatus.filled.value
        self.sts_canceled = QuoteStatus.canceled.value
        self.gateway_side_sell = constants.GatewaySide.Sell
        self.status = constants.Status.Fill

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_rfq_params()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency=self.currency, Instrument=self.instrument_spot,
                                                      OrderQty=self.qty)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 2
        self.quote_request_book.set_filter(
            [self.cur_column, self.currency, self.qty_column, self.qty]).check_quote_book_fields_list({
            self.sts_column: self.sts_new, self.quote_status_column: self.sts_accepted})
        # endregion
        # region Step 3
        self.quote_request_book.set_filter(
            [self.cur_column, self.currency, self.qty_column, self.qty]).check_2nd_lvl_quote_book_fields_list(
            {self.quote_status_column: self.sts_accepted}, event_name="Check Quote Accepted")
        # endregion
        # region Step 4
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
        self.quote_request_book.set_filter(
            [self.cur_column, self.currency, self.qty_column, self.qty]).check_2nd_lvl_quote_book_fields_list(
            {self.quote_status_column: self.sts_filled}, event_name="Check Quote Filled")
        # endregion
        # region Step 5
        quote_request.set_rfq_params_fwd()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency=self.currency, Instrument=self.instrument_fwd,
                                                      OrderQty=self.qty)
        response = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote_fwd(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        self.quote_request_book.set_filter(
            [self.cur_column, self.currency, self.qty_column, self.qty]).check_2nd_lvl_quote_book_fields_list(
            {self.quote_status_column: self.sts_accepted}, event_name="Check Quote Accepted")
        # endregion
        # region  Step 6
        quote_cancel = FixMessageQuoteCancelFX().set_params_for_cancel(quote_request, response[0])
        self.fix_manager_gtw.send_message(quote_cancel)
        self.quote_request_book.set_filter(
            [self.cur_column, self.currency, self.qty_column, self.qty]).check_2nd_lvl_quote_book_fields_list(
            {self.quote_status_column: self.sts_canceled}, event_name="Check Quote Canceled")
        # endregion
