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
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_3741(TestCase):
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
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_1 = self.data_set.get_settle_date_by_name("broken_2")
        self.settle_date_2 = self.data_set.get_settle_date_by_name("broken_w1w2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type = self.data_set.get_settle_type_by_name("broken")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")

        self.qty = random_qty(1, 7, 7)

        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_qty=self.qty, settle_type=self.settle_type,
                                           settle_date=self.settle_date_1, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_far_leg(leg_qty=self.qty, settle_type=self.settle_type,
                                          settle_date=self.settle_date_2, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
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
        self.quote.set_params_for_quote_swap(self.quote_request)
        quote_response = next(response)
        quote_from_di = self.fix_manager_sel.parse_response(quote_response)[0]
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        self.new_order_single.set_default_prev_quoted_swap(self.quote_request, quote_from_di, side="1")
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_swap(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
