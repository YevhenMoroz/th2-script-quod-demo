from pathlib import Path
from custom import basic_custom_actions as bca
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
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Status
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook


class QAP_1562(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.quote_order_book = FXOrderBook(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument_spot = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.qty1 = random_qty(1, 2, 7)
        self.qty2 = random_qty(1, 2, 7)
        self.qty_column = OrderBookColumns.qty.value
        self.sts_column = OrderBookColumns.sts.value
        self.sts_rejected = Status.rejected.value
        self.status = constants.Status.Reject

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_rfq_params()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency=self.currency, Instrument=self.instrument_spot,
                                                      OrderQty=self.qty1)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        # endregion

        # region Step 2-3
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_prev_quoted(quote_request, response[0])
        new_order_single.change_parameter("OrderQty", self.qty2)
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        # endregion

        # region Step 4-5
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
        self.quote_order_book.set_filter(
            [self.qty_column, self.qty2]).check_order_fields_list({self.sts_column: self.sts_rejected})
        # endregion

