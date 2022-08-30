from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX


class QAP_T2543(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.gbp_xxx = "GBP/XXX"
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.instrument_spot = {
            'Symbol': self.gbp_xxx,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.instrument_spot,
            'SettlType': self.settle_type_spot}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        # region Step 2
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_reject.set_md_reject_params(self.md_request, text="no active client tier")
        self.fix_verifier.check_fix_message(fix_message=self.md_reject)
        # endregion
