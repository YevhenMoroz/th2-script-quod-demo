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
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2564(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.client_column = QuoteRequestBookColumns.client.value

        self.qty_40m = random_qty(4, 5, 8)
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.sec_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.eur_gbp_swap = {
            "Symbol": self.eur_gbp,
            "SecurityType": self.sec_type_swap}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd().update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                                              Account=self.iridium1,
                                                                              Instrument=self.eur_gbp_swap)
        self.quote_request.update_near_leg(leg_symbol=self.eur_gbp)
        self.quote_request.update_far_leg(leg_symbol=self.eur_gbp)
        self.quote_request.remove_fields_in_repeating_group("NoRelatedSymbols", ["Side"])
        response = self.fix_manager.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # endregion

        # region Step 2
        self.dealer_intervention.set_list_filter([self.client_column, self.iridium1]).assign_quote(1)
        self.dealer_intervention.estimate_quote()
        time.sleep(10)
        self.dealer_intervention.send_quote()
        time.sleep(2)
        self.dealer_intervention.close_window()

        self.quote.set_params_for_quote_swap(self.quote_request)
        quote_response = next(response)
        quote_from_di = self.fix_manager.parse_response(quote_response)[0]
        self.new_order_single.set_default_for_dealer_swap(self.quote_request, quote_from_di)
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        # endregion

        # region Step 3
        self.execution_report.set_params_from_new_order_swap(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
