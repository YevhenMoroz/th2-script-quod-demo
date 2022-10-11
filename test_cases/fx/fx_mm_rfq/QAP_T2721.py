import random
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
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, RFQPanelPtsAndPx


class QAP_T2721(TestCase):
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
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.qty = str(random.randint(54000000, 55000000))
        self.ex_ask_small = PriceNaming.ask_pips
        self.ex_ask_large = PriceNaming.ask_large
        self.ask_pts = RFQPanelPtsAndPx.ask_near_points_value_label
        self.ask_px = RFQPanelPtsAndPx.ask_value_label
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument,
                                                           OrderQty=self.qty)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region step 2
        self.dealer_intervention.set_list_filter(["Qty", self.qty])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        # endregion
        # region step 3
        extracted_qty = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_ask_large,
                                                                                     self.ex_ask_small)
        ask_large = extracted_qty[self.ex_ask_large.value]
        ask_small = extracted_qty[self.ex_ask_small.value]
        expected_ask_qty = ask_large+ask_small

        extracted_pts_px = self.dealer_intervention.extract_px_and_pts_from_di_panel(self.ask_pts, self.ask_px)
        ask_pts = extracted_pts_px[self.ask_pts.value]
        ask_px = extracted_pts_px[self.ask_px.value]
        offer_px = str(float(expected_ask_qty)+(float(ask_pts)/10000))

        self.dealer_intervention.compare_values(expected_value=ask_px, actual_value=offer_px,
                                                event_name="Compare pts and px ask values")
        self.dealer_intervention.close_window()
        # endregion
