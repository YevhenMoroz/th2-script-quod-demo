from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2650(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.md_snapshot_2 = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.web_adm_env.session_alias_wa, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.gbp_aud = self.data_set.get_symbol_by_name('symbol_9')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.client_tier_palladium1 = self.data_set.get_client_tier_id_by_name("client_tier_id_4")
        self.client_palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.instrument_fwd = {
            'Symbol': self.gbp_aud,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols_1w = [{
            'Instrument': self.instrument_fwd,
            'SettlType': self.settle_type_1w}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 3
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client_palladium1)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_1w)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion
        # region Step 4-5
        self.rest_massage.find_client_tier_instrument(self.client_tier_palladium1, self.gbp_aud)
        params_gbp_aud = self.rest_manager.send_get_request_filtered(self.rest_massage)
        params_gbp_aud = self.rest_manager. \
            parse_response_details(params_gbp_aud,
                                   {'clientTierID': self.client_tier_palladium1, 'instrSymbol': self.gbp_aud})

        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_gbp_aud). \
            update_value_in_component('clientTierInstrSymbolFwdVenue', 'excludeWhenUnhealthy',
                                      'true', {'venueID': 'BARX'})
        self.rest_manager.send_post_request(self.rest_massage)
        # endregion
        # region Step 6
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client_palladium1)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_1w)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot_2.set_params_for_empty_md_response(self.md_request, ["*"])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 5
        self.rest_massage.modify_client_tier_instrument(). \
            update_value_in_component('clientTierInstrSymbolFwdVenue', 'excludeWhenUnhealthy',
                                      'false', {'venueID': 'BARX'})
        self.rest_manager.send_post_request(self.rest_massage)
        # endregion
