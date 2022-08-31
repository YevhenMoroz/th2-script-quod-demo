import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2549(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_2")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.settle_type_wk3 = self.data_set.get_settle_type_by_name("wk3")
        self.settle_date_wk3 = self.data_set.get_settle_date_by_name("wk3")

        self.qty = random_qty(2, 5, 8)

        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                                Account=self.account,
                                                                                Currency=self.currency,
                                                                                Instrument=self.instrument,
                                                                                SettlDate=self.settle_date_wk3,
                                                                                SettlType=self.settle_type_wk3,
                                                                                OrderQty=self.qty)
        response = self.fix_manager_sel.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # endregion

        # region Step 2
        client_column = QuoteRequestBookColumns.client.value
        self.dealer_intervention.set_list_filter([client_column, self.account]).assign_quote(1)
        self.dealer_intervention.estimate_quote()
        time.sleep(10)
        self.dealer_intervention.send_quote()
        time.sleep(2)
        self.dealer_intervention.close_window()
        # endregion
        # region Step 3
        self.quote.set_params_for_dealer(self.quote_request)
        quote_response = next(response)
        quote_from_di = self.fix_manager_sel.parse_response(quote_response)[0]
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        self.new_order_single.set_default_prev_quoted(self.quote_request, quote_from_di)
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        # endregion
        # region Step 4
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
