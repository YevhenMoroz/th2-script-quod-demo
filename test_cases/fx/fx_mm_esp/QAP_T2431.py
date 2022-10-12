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
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2431(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.client_tier_silver = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.web_adm_env, self.test_id)
        self.rest_manager_doubler = RestApiManager(self.web_adm_env, self.test_id)
        self.rest_message = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.rest_message_doubler = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.params_eur_usd_reserved = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rest_message.find_all_client_tier_instrument()
        params_eur_usd = self.rest_manager.send_get_request(self.rest_message)
        self.params_eur_usd_reserved = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_silver, 'instrSymbol': self.eur_usd})
        self.sleep(4)
        params_eur_usd = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_silver, 'instrSymbol': self.eur_usd})
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            params_eur_usd).add_sweepable_qty("1000000")
        self.rest_manager.send_post_request(self.rest_message)
        self.sleep(4)
        self.rest_message_doubler.find_all_client_tier_instrument()
        params_eur_usd = self.rest_manager_doubler.send_get_request(self.rest_message_doubler)
        params_eur_usd = self.rest_manager_doubler. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_silver, 'instrSymbol': self.eur_usd})
        self.rest_message_doubler.clear_message_params().modify_client_tier_instrument().set_params(
            params_eur_usd).add_sweepable_qty("1000000")
        self.rest_manager_doubler.send_post_request(self.rest_message_doubler)
        self.sleep(10)
        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "1000000", "1000000"])
        self.sleep(4)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params_eur_usd_reserved)
        self.rest_manager.send_post_request(self.rest_message)
