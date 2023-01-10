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


class QAP_T2462(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.security_type_spot,
                'Product': '4'}}]
        self.no_related_symbols_check = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.security_type_spot,
                'Product': '4'}, 'SettlType': ''}]
        self.bands = ["1000000", '5000000', '10000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-3
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.silver}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_subscribe.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_check)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands)
        self.fix_verifier.check_fix_message(self.fix_md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region step 4
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe)
        # endregion
