import time
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T2413(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_esp_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.modify_client_tier = RestApiClientTierMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_esp_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_esp_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type = self.data_set.get_settle_type_by_name("today")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.msg_prams = None
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.gbp_usd,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type, }]
        self.bands_gbp_usd = ["1000000"]
        self.minus_2 = (datetime.now() - timedelta(hours=2))
        self.minus_1 = (datetime.now() - timedelta(hours=1))
        self.timestamp_2 = str(datetime.timestamp(self.minus_2)).replace(".", "")[:13]
        self.timestamp_1 = str(datetime.timestamp(self.minus_1)).replace(".", "")[:13]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_client_tier.find_client_tier(self.client_id)
        self.msg_prams = self.rest_manager.send_get_request_filtered(self.modify_client_tier)
        self.msg_prams = self.rest_manager.parse_response_details(self.msg_prams, {"clientTierID": self.client_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams) \
            .add_parameters({"TODStartTime": self.timestamp_2, "TODEndTime": self.timestamp_1})
        self.rest_manager.send_post_request(self.modify_client_tier)
        time.sleep(5)
        # endregion
        # region Step 2
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        # endregion
        # region Step 3
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_gbp_usd, published=False, response=response[0])
        self.fix_verifier.check_fix_message(self.fix_md_snapshot)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, "Unsubscribe")
        self.modify_client_tier.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.sleep(2)
