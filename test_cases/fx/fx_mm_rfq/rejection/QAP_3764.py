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


class QAP_3764(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.rfq_reject = FixMessageQuoteRequestRejectFX(data_set=self.data_set)
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.sec_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.wk3_date = self.data_set.get_settle_date_by_name('wk3')
        self.client_iridium = self.data_set.get_client_by_name("client_mm_3")

        self.instrument = {
            "Symbol": self.eur_usd,
            "SecurityType": self.sec_type_fwd}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                            Account=self.client_iridium,
                                                                            Instrument=self.instrument,
                                                                            SettlDate=self.wk3_date)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.rfq_reject.set_quote_reject_params(self.quote_request, text="no RFS venue available")
        self.fix_verifier.check_fix_message(fix_message=self.rfq_reject)
        # endregion
