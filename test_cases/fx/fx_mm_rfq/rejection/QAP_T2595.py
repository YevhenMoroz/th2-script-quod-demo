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
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2595(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.client_column = QuoteRequestBookColumns.client.value

        self.qty_40m = random_qty(4, 5, 8)
        self.client_argentina = self.data_set.get_client_by_name("client_mm_2")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.sec_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.eur_gbp_swap = {
            "Symbol": self.eur_gbp,
            "SecurityType": self.sec_type_swap}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                              Account=self.client_argentina,
                                                                              Instrument=self.eur_gbp_swap)
        self.quote_request.update_near_leg(leg_symbol=self.eur_gbp, leg_qty=self.qty_40m)
        self.quote_request.update_far_leg(leg_symbol=self.eur_gbp, leg_qty=self.qty_40m)
        response = self.fix_manager.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # endregion

        # region Step 2
        self.dealer_intervention.set_list_filter([self.client_column, self.client_argentina]).assign_quote(1)
        self.dealer_intervention.estimate_quote()
        time.sleep(10)
        self.dealer_intervention.send_quote()
        time.sleep(2)
        self.dealer_intervention.close_window()

        self.quote.set_params_for_quote_swap(self.quote_request)
        next(response)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
