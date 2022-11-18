from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2519(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.quote = FixMessageQuoteFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.eur_jpy = self.data_set.get_symbol_by_name("symbol_4")
        self.qty_300m = "300000000"
        self.acc_iridium = self.data_set.get_client_by_name("client_mm_3")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.instr_eur_jpy = {"Symbol": self.eur_jpy,
                           "SecurityType": self.security_type_swap}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.acc_iridium,
                                                           Instrument=self.instr_eur_jpy)
        self.quote_request.update_near_leg(leg_qty=self.qty_300m, leg_symbol=self.eur_jpy)
        self.quote_request.update_far_leg(leg_qty=self.qty_300m, leg_symbol=self.eur_jpy)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote,
                                            key_parameters=["QuoteReqID"])
        # endregion
