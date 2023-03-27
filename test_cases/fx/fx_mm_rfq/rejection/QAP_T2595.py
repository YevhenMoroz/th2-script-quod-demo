from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty, extract_automatic_quoting
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2595(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.verifier = Verifier(self.test_id)
        self.qty = random_qty(9, len=9)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.iridium1)
        self.quote_request.update_near_leg(leg_qty=self.qty)
        self.quote_request.update_far_leg(leg_qty=self.qty)
        self.quote_request.get_parameter("NoRelatedSymbols")[0].pop("Side")
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].pop("LegSide")
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].pop("LegSide")
        self.fix_manager.send_message(self.quote_request)
        automatic_quoting = extract_automatic_quoting(self.quote_request)
        self.verifier.set_event_name("Check quote presence in DI")
        self.verifier.compare_values("Check quote presence in DI", "N",  automatic_quoting)
        self.verifier.verify()

