import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2457(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.rest_env.session_alias_wa, self.test_id)
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.params_eur_usd = None
        self.nok_sek = self.data_set.get_symbol_by_name('symbol_synth_1')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.settle_type = self.data_set.get_settle_type_by_name('spot')
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': self.nok_sek,
                'SecurityType': self.data_set.get_security_type_by_name('fx_spot'),
                'Product': '4', },
            'SettlType': self.settle_type, }]
        self.bands = ["1000000", "10000000"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rest_massage.find_client_tier_instrument('3200016', self.eur_usd)
        self.params_eur_usd = self.rest_manager.send_get_request_filtered(self.rest_massage)
        self.params_eur_usd = self.rest_manager. \
            parse_response_details(self.params_eur_usd,
                                   {'clientTierID': '3200016', 'instrSymbol': self.eur_usd})
        # endregion

        # region Step 2
        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(self.params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'IND', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        time.sleep(2)
        # endregion

        # region Step 3
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.data_set.get_client_by_name('client_mm_11')}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands, published=False, response=response[0])
        self.fix_md_snapshot.get_parameter("NoMDEntries").pop(3)
        self.fix_verifier.check_fix_message(self.fix_md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(self.params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'TRD', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion
        self.sleep(2)
