import time
from pathlib import Path
from random import randint
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.fe_trading_constant import RFQPanelPtsAndPx


class QAP_T2391(TestCase):
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
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.settle_date_today = self.data_set.get_settle_date_by_name("today")
        self.settle_date_tom = self.data_set.get_settle_date_by_name("tomorrow")
        self.settle_type_today = self.data_set.get_settle_type_by_name("today")
        self.settle_type_tom = self.data_set.get_settle_type_by_name("tomorrow")
        self.ask_far_pts = RFQPanelPtsAndPx.ask_far_points_value_label
        self.bid_far_pts = RFQPanelPtsAndPx.bid_far_points_value_label
        self.qty = str(randint(10000000, 11000000))
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.account, Currency=self.currency,
                                                           Instrument=self.instrument)
        self.quote_request.remove_fields_in_repeating_group("NoRelatedSymbols", ["Side"])
        self.quote_request.update_near_leg(leg_symbol=self.symbol, settle_type=self.settle_type_today,
                                           leg_qty=self.qty, settle_date=self.settle_date_today)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, settle_type=self.settle_type_tom,
                                          leg_qty=self.qty, settle_date=self.settle_date_tom)
        response = self.fix_manager_sel.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        self.dealer_intervention.set_list_filter(["NearLegQty", self.qty, "FarLegQty", self.qty])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        extracted_ask_far_pts = self.dealer_intervention.extract_px_and_pts_from_di_panel(self.ask_far_pts)
        extracted_bid_far_pts = self.dealer_intervention.extract_px_and_pts_from_di_panel(self.bid_far_pts)
        ask_far_pts = extracted_ask_far_pts[self.ask_far_pts.value]
        bid_far_pts = extracted_bid_far_pts[self.bid_far_pts.value]
        self.dealer_intervention.send_quote()
        quote_response = next(response)
        quote_from_di = self.fix_manager_sel.parse_response(quote_response)[0]
        far_bid_pts = quote_from_di.get_parameter("NoLegs")[1]["LegBidForwardPoints"]
        far_offer_pts = quote_from_di.get_parameter("NoLegs")[1]["LegOfferForwardPoints"]
        # endregion
        # region step 3
        self.dealer_intervention.compare_values(expected_value=ask_far_pts, actual_value=far_offer_pts,
                                                event_name="Compare DI ask pts")
        self.dealer_intervention.compare_values(expected_value=far_bid_pts, actual_value=bid_far_pts,
                                                event_name="Compare DI bid pts")
        self.dealer_intervention.close_window()
        # endregion
