from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2458(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.usd_php = self.data_set.get_symbol_by_name('symbol_ndf_1')
        self.sec_type_ndf = self.data_set.get_security_type_by_name("fx_ndf")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.instrument = {
            'Symbol': self.usd_php,
            'SecurityType': self.sec_type_ndf,
            'Product': '4', }
        self.verify_instrument = {"Symbol": self.usd_php, "MaturityDate": "*"}
        self.no_related_symbols = [{
            "Instrument": self.instrument,
            "SettlType": self.settle_type_1w
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium1)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, response=response[0])
        self.md_snapshot.change_parameter("Instrument", self.verify_instrument)
        # endregion

        # region Step 2
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 3
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
        self.sleep(2)
