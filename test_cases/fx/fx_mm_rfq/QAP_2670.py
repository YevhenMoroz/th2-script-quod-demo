import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets import constants
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns, Status
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_2670(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_rfq_connectivity
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.rest_manager = RestApiManager(self.ss_connectivity, self.test_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument_spot = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.qty = random_qty(2, 5, 8)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.qty_column = QuoteRequestBookColumns.qty.value
        self.sts_column = QuoteRequestBookColumns.status.value
        self.cur_column = QuoteRequestBookColumns.currency.value
        self.sts_new = Status.new.value
        self.status = constants.Status.Fill
        self.quote_response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        quote_request = FixMessageQuoteRequestFX().set_rfq_params()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency=self.currency, Instrument=self.instrument_spot,
                                                      OrderQty=self.qty, Side="2")
        response = self.fix_manager_gtw.send_quote_to_dealer_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_dealer(quote_request)
        # endregion
        # region Step 2
        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.qty, self.cur_column, self.currency]).check_unassigned_fields(
            {self.sts_column: self.sts_new})
        self.dealer_intervention.assign_quote()
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        self.dealer_intervention.send_quote()

        self.quote_response = next(response)
        quote_from_di = self.fix_manager_gtw.parse_response(self.quote_response)[0]
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 3
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_for_dealer(quote_request, quote_from_di)
        self.fix_manager_gtw.send_message_and_receive_response(new_order_single)
        execution_report = FixMessageExecutionReportPrevQuotedFX().set_params_from_new_order_single(new_order_single,
                                                                                                    self.status)
        self.fix_verifier.check_fix_message(execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.dealer_intervention.close_window()
