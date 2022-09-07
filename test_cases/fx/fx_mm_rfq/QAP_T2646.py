import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, RFQPanelQty


class QAP_T2646(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.near_leg_quantity = RFQPanelQty.opposite_near_bid_qty_value_label
        self.near_qty = "21000000"
        self.far_qty = "23000000"
        self.ex_bid_small = PriceNaming.bid_pips
        self.ex_bid_large = PriceNaming.bid_large
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_qty=self.near_qty)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_qty=self.far_qty)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        self.dealer_intervention.set_list_filter(["NearLegQty", self.near_qty, "FarLegQty", self.far_qty])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        extracted_values = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_bid_large,
                                                                                        self.ex_bid_small)
        bid_large = extracted_values[self.ex_bid_large.value]
        bid_small = extracted_values[self.ex_bid_small.value]
        expected_bid_qty = str(round(float(bid_large+bid_small)*(float(self.near_qty)/1000000), 2))+"M USD"
        extracted_near_leg_quantity = self.dealer_intervention.extract_qty_from_di_panel(self.near_leg_quantity)
        near_qty = extracted_near_leg_quantity[self.near_leg_quantity.value]
        self.dealer_intervention.compare_values(expected_value=expected_bid_qty, actual_value=near_qty,
                                                event_name="Compare DI bid near qty value")
        self.dealer_intervention.close_window()
        # endregion
