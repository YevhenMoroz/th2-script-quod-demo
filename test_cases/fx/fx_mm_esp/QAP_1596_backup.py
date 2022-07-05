import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiQuotingSessionMessages import RestApiQuotingSessionMessages


class QAP_1596(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.rest_manager = RestApiManager(self.adm_env.session_alias_wa, self.test_id)
        self.rest_massage = RestApiQuotingSessionMessages()
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.verifier = Verifier(self.test_id)
        self.mdentryid_event = "Always new MDEntryID"

        self.nok_sek = self.data_set.get_symbol_by_name('symbol_synth_1')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.settle_type = self.data_set.get_settle_type_by_name('spot')
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': self.nok_sek,
                'SecurityType': self.data_set.get_security_type_by_name('fx_spot'),
                'Product': '4', },
            'SettlType': self.settle_type, }]
        self.bands = ["1000000", '3000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Test variables
        # print(self.adm_env.session_alias_wa)
        # endregion
        # region Step 1
        self.rest_massage.set_default_params_esp().enable_always_new_mdentryid()
        self.rest_manager.send_post_request(self.rest_massage)
        # params_eur_usd = self.rest_manager.send_get_request(self.rest_massage)
        # params_eur_usd = self.rest_manager. \
        #     parse_response_details(params_eur_usd,
        #     {'clientTierID': '2000011', 'instrSymbol': self.eur_usd})
        #     # endregion
        #
        #     # region Step 2
        #     self.rest_massage.clear_message_params().modify_client_tier_instrument() \
        #         .set_params(params_eur_usd). \
        #         update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'IND', {'tenor': 'SPO'})
        #     self.rest_manager.send_post_request(self.rest_massage)
        # endregion
        time.sleep(10)
        # region Step 3
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.data_set.get_client_by_name('client_mm_5')}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        # self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        no_md_entries = response[0].get_parameter("NoMDEntries")
        md_entry_id_1 = no_md_entries[0].get("MDEntryID")
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        no_md_entries = response[0].get_parameter("NoMDEntries")
        md_entry_id_2 = no_md_entries[0].get("MDEntryID")
        self.verifier.set_event_name(self.mdentryid_event)
        self.verifier.compare_values(self.mdentryid_event, md_entry_id_1, md_entry_id_2, verification_method=VerificationMethod.NOT_EQUALS)
        self.verifier.verify()

        # print(self.fix_manager_gtw.send_message_and_receive_response_fix_standard(self.fix_subscribe))

        # endregion

        # region Postconditions

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_massage.set_default_params_esp()
        self.rest_manager.send_post_request(self.rest_massage)
        # self.rest_massage.set_default_params_esp().set_update_type_fullrefresh()
        # self.rest_manager.send_post_request(self.rest_massage)
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion
