from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T8694(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.free_notes_column = OrderBookColumns.free_notes.value
        self.qty_column = OrderBookColumns.qty.value
        self.client_column = QuoteRequestBookColumns.client.value
        self.presence_event = "Order presence check"
        self.expected_free_notes = "failed to get forward points through RFQ - manual intervention required"

        self.qty_4m = random_qty(4, 5, 7)
        self.qty_5m = random_qty(5, 6, 7)
        self.expected_qty = ""
        self.client_argentina = self.data_set.get_client_by_name("client_mm_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.quote_request.set_swap_fwd_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                              Account=self.client_argentina)
        self.quote_request.update_near_leg(leg_qty=self.qty_4m)
        self.quote_request.update_far_leg(leg_qty=self.qty_5m)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)

        actual_qty = self.dealer_intervention.extract_field_from_unassigned(self.qty_column)
        self.dealer_intervention.compare_values("", actual_qty, self.presence_event)

        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.expected_qty, self.client_column, self.client_argentina])
        actual_free_notes = self.dealer_intervention.extract_field_from_unassigned(self.free_notes_column)
        self.dealer_intervention.compare_values(self.expected_free_notes, actual_free_notes, self.presence_event)
        # endregion
