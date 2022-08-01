import random
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2906(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.qty = str(random.randint(50000000, 51000000))
        self.ttl = "360"
        self.bid_large = "1.11"
        self.bid_small = "111"
        self.ask_large = "1.23"
        self.ask_small = "456"
        self.ex_ttl = PriceNaming.ttl
        self.ex_bid_small = PriceNaming.bid_pips
        self.ex_bid_large = PriceNaming.bid_large
        self.ex_ask_small = PriceNaming.ask_pips
        self.ex_ask_large = PriceNaming.ask_large
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty, Account=self.account,
                                                           Instrument=self.instrument, Currency=self.currency)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        self.dealer_intervention.set_list_filter(["Qty", self.qty])
        self.dealer_intervention.assign_quote(row_number=1)
        time.sleep(5)
        self.dealer_intervention.estimate_quote()
        time.sleep(5)
        # region step 2-3
        self.dealer_intervention.set_price_and_ttl(ttl=self.ttl, bid_large=self.bid_large, bid_small=self.bid_small,
                                                   ask_large=self.ask_large, ask_small=self.ask_small)
        extracted_ttl = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_ttl)
        ttl = extracted_ttl[self.ex_ttl.value]
        self.dealer_intervention.compare_values(expected_value=self.ttl, actual_value=ttl,
                                                event_name="Compare DI ttl value")
        # endregion
        # region step 4-5
        # Check skew towards bid, decrease bid, decrease ask
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.skew_towards_bid)
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.decrease_bid)
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.decrease_ask)

        extracted_ask_bid_small = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_bid_small,
                                                                                               self.ex_ask_small)
        bid_small = extracted_ask_bid_small[self.ex_bid_small.value]
        ask_small = extracted_ask_bid_small[self.ex_ask_small.value]
        self.dealer_intervention.compare_values(expected_value=str(int(self.bid_small) + 20), actual_value=bid_small,
                                                event_name="Compare DI skew towards bid value",
                                                ver_method=VerificationMethod.EQUALS)
        self.dealer_intervention.compare_values(expected_value=str(int(self.ask_small) - 20), actual_value=ask_small,
                                                event_name="Compare DI skew towards ask value",
                                                ver_method=VerificationMethod.EQUALS)
        # endregion
        # region step 6-8
        # Check skew towards ask, increase bid, increase ask
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.skew_towards_ask)
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.increase_bid)
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.increase_ask)

        extracted_ask_bid_small_2 = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_bid_small,
                                                                                                 self.ex_ask_small)
        bid_small = extracted_ask_bid_small_2[self.ex_bid_small.value]
        ask_small = extracted_ask_bid_small_2[self.ex_ask_small.value]
        self.dealer_intervention.compare_values(expected_value=str(int(self.bid_small)-20), actual_value=bid_small,
                                                event_name="Compare DI skew towards bid value",
                                                ver_method=VerificationMethod.EQUALS)
        self.dealer_intervention.compare_values(expected_value=str(int(self.ask_small)+20), actual_value=ask_small,
                                                event_name="Compare DI skew towards ask value",
                                                ver_method=VerificationMethod.EQUALS)
        # endregion
        # region step 9-10
        # Check widen spread
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.widen_spread)
        extracted_ask_bid_small_3 = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_bid_small,
                                                                                                 self.ex_ask_small)
        bid_small = extracted_ask_bid_small_3[self.ex_bid_small.value]
        ask_small = extracted_ask_bid_small_3[self.ex_ask_small.value]
        self.dealer_intervention.compare_values(expected_value=str(int(self.bid_small) + 10), actual_value=bid_small,
                                                event_name="Compare DI widen spread bid value",
                                                ver_method=VerificationMethod.EQUALS)
        self.dealer_intervention.compare_values(expected_value=str(int(self.ask_small) + 10), actual_value=ask_small,
                                                event_name="Compare DI widen spread ask value",
                                                ver_method=VerificationMethod.EQUALS)
        # Check narrow spread
        self.dealer_intervention.modify_spread(ClientPrisingTileAction.narrow_spread)
        extracted_ask_bid_small_4 = self.dealer_intervention.extract_price_and_ttl_from_di_panel(self.ex_bid_small,
                                                                                                 self.ex_ask_small)
        bid_small = extracted_ask_bid_small_4[self.ex_bid_small.value]
        ask_small = extracted_ask_bid_small_4[self.ex_ask_small.value]
        self.dealer_intervention.compare_values(expected_value=str(int(self.bid_small) - 10), actual_value=bid_small,
                                                event_name="Compare DI narrow spread bid value",
                                                ver_method=VerificationMethod.EQUALS)
        self.dealer_intervention.compare_values(expected_value=str(int(self.ask_small) - 10), actual_value=ask_small,
                                                event_name="Compare DI narrow spread ask value",
                                                ver_method=VerificationMethod.EQUALS)
        self.dealer_intervention.close_window()
        # endregion
