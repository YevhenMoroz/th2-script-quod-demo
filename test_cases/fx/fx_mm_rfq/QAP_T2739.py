import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.fe_trading_constant import RFQPanelQty


class QAP_T2739(TestCase):
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
        self.near_leg_quantity = RFQPanelQty.near_leg_quantity
        self.far_leg_quantity = RFQPanelQty.far_leg_quantity
        self.qty_thousand_1 = random_qty(1, 10, 6)
        self.qty_thousand_2 = random_qty(1, 10, 6)
        self.qty_millions_1 = random_qty(1, 10, 9)
        self.qty_millions_2 = random_qty(1, 10, 9)
        self.qty_billions_1 = random_qty(1, 10, 12)
        self.qty_billions_2 = random_qty(1, 10, 12)
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_qty=self.qty_thousand_1)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_qty=self.qty_thousand_2)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 2
        self.dealer_intervention.set_list_filter(["NearLegQty", self.qty_thousand_1, "FarLegQty", self.qty_thousand_2])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        expected_qty_thousand_1 = str(float(self.qty_thousand_1) / 1000) + " GBP"
        expected_qty_thousand_2 = str(float(self.qty_thousand_2) / 1000) + " GBP"

        extracted_legs_quantity = self.dealer_intervention.extract_qty_from_di_panel(self.near_leg_quantity,
                                                                                     self.far_leg_quantity)
        near_qty = extracted_legs_quantity[self.near_leg_quantity.value]
        far_qty = extracted_legs_quantity[self.far_leg_quantity.value]
        self.dealer_intervention.compare_values(expected_value=expected_qty_thousand_1, actual_value=near_qty,
                                                event_name="Compare near qty in thousands value")
        self.dealer_intervention.compare_values(expected_value=expected_qty_thousand_2, actual_value=far_qty,
                                                event_name="Compare far qty in thousands value")
        self.dealer_intervention.close_window()
        # endregion
        # region step 3
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_qty=self.qty_millions_1)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_qty=self.qty_millions_2)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 4
        self.dealer_intervention.set_list_filter(["NearLegQty", self.qty_millions_1, "FarLegQty", self.qty_millions_2])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        expected_qty_millions_1 = str(float(self.qty_millions_1) / 1000000)[:6] + "M GBP"
        expected_qty_millions_2 = str(float(self.qty_millions_2) / 1000000)[:6] + "M GBP"

        extracted_legs_quantity = self.dealer_intervention.extract_qty_from_di_panel(self.near_leg_quantity,
                                                                                     self.far_leg_quantity)
        near_qty = extracted_legs_quantity[self.near_leg_quantity.value]
        far_qty = extracted_legs_quantity[self.far_leg_quantity.value]
        self.dealer_intervention.compare_values(expected_value=expected_qty_millions_1, actual_value=near_qty,
                                                event_name="Compare near qty in millions value")
        self.dealer_intervention.compare_values(expected_value=expected_qty_millions_2, actual_value=far_qty,
                                                event_name="Compare far qty in millions value")
        self.dealer_intervention.close_window()
        # endregion
        # region step 5
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_qty=self.qty_billions_1)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_qty=self.qty_billions_2)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 6
        self.dealer_intervention.set_list_filter(["NearLegQty", self.qty_billions_1, "FarLegQty", self.qty_billions_2])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        expected_qty_billions_1 = str(float(self.qty_billions_1) / 1000000000)[:6] + "B GBP"
        expected_qty_billions_2 = str(float(self.qty_billions_2) / 1000000000)[:6] + "B GBP"

        extracted_legs_quantity = self.dealer_intervention.extract_qty_from_di_panel(self.near_leg_quantity,
                                                                                     self.far_leg_quantity)
        near_qty = extracted_legs_quantity[self.near_leg_quantity.value]
        far_qty = extracted_legs_quantity[self.far_leg_quantity.value]
        self.dealer_intervention.compare_values(expected_value=expected_qty_billions_1, actual_value=near_qty,
                                                event_name="Compare near qty in billions value")
        self.dealer_intervention.compare_values(expected_value=expected_qty_billions_2, actual_value=far_qty,
                                                event_name="Compare far qty in billions value")
        self.dealer_intervention.close_window()
        # endregion

