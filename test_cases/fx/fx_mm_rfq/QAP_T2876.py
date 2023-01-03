from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class QAP_T2876(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject= FixMessageQuoteRequestRejectFX()
        self.acc_iridium = self.data_set.get_client_by_name("client_mm_3")
        self.incorrect_symbol = "USS/GGB"
        self.php = self.data_set.get_currency_by_name("currency_php")
        self.security_type_nds = self.data_set.get_security_type_by_name("fx_nds")
        self.instrument = {
            "Symbol": self.incorrect_symbol,
            "SecurityType": self.security_type_nds}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_ndf()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.acc_iridium,
                                                           Instrument=self.instrument)
        self.quote_request.update_near_leg(leg_symbol=self.incorrect_symbol)
        self.quote_request.update_far_leg(leg_symbol=self.incorrect_symbol)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 2
        text = "11620 Unknown instrument"
        self.quote_reject.set_quote_reject_swap(self.quote_request, text=text)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account"])
        self.fix_verifier.check_fix_message(self.quote_reject)
        # endregion

