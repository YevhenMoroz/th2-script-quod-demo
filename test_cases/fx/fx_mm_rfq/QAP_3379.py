from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_3379(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_rfq_connectivity = self.fix_env.sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)

        self.qty_event = "qty verification"

        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        # iridium1 aud/usd
        self.account = self.data_set.get_client_by_name("client_mm_4")
        self.symbol_1 = self.data_set.get_symbol_by_name("symbol_3")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")

        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_2w = self.data_set.get_settle_date_by_name("wk2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.settle_type_2w = self.data_set.get_settle_type_by_name("wk2")
        # self.qty = random_qty(1, 3, 7)
        self.qty_1 = "999999"
        self.qty_2 = "999999999"
        self.price = "*"
        self.instrument = {
            "Symbol": self.symbol_1,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_qty=self.qty_1, leg_symbol=self.symbol_1,
                                           settle_type=self.settle_type_1w,
                                           settle_date=self.settle_date_1w, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_far_leg(leg_qty=self.qty_1, leg_symbol=self.symbol_1,
                                           settle_type=self.settle_type_2w,
                                           settle_date=self.settle_date_2w, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="EUR", Instrument=self.instrument,
                                                           OrderQty=self.qty_1)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion

        # region Step 2
        self.dealer_intervention.assign_quote(1)
        # endregion

        # region Step 3
        self.dealer_intervention.estimate_quote()
        expected_price = self.dealer_intervention.extract_price_and_ttl_from_di_panel()
        self.verifier.compare_values(self.qty_event, self.price, expected_price)
        self.verifier.verify()
        # endregion

        # region Step 4
        expected_qty = self.dealer_intervention.extract_qty_from_di_panel()
        self.verifier.compare_values(self.qty_event, self.qty_1, expected_qty)
        self.verifier.verify()
        # endregion

        # region Step 5
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_qty=self.qty_2, leg_symbol=self.symbol_1,
                                           settle_type=self.settle_type_spot,
                                           settle_date=self.settle_date_spot, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_far_leg(leg_qty=self.qty_2, leg_symbol=self.symbol_1,
                                           settle_type=self.settle_type_1w,
                                           settle_date=self.settle_date_1w, leg_sec_type=self.security_type_fwd)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="EUR", Instrument=self.instrument,
                                                           OrderQty=self.qty_2)
        self.fix_manager_sel.send_message(self.quote_request)

        self.dealer_intervention.assign_quote(1)
        self.dealer_intervention.estimate_quote()

        expected_price = self.dealer_intervention.extract_price_and_ttl_from_di_panel()
        self.verifier.compare_values(self.qty_event, self.price, expected_price)
        self.verifier.verify()

        expected_qty = self.dealer_intervention.extract_qty_from_di_panel()
        self.verifier.compare_values(self.qty_event, self.qty_2, expected_qty)
        self.verifier.verify()
        # endregion
