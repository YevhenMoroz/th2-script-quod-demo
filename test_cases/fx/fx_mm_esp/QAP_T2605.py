from datetime import datetime
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T2605(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.modify_client_tier = RestApiClientTierMessages()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.msg_prams_client = None
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.book_type_tiered = "1"
        self.client_id_silver = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.instrument_spot = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.instrument_spot,
            'SettlType': self.settle_type_spot}]
        self.md_entry_date = datetime.utcnow().strftime('%Y%m%d')
        self.md_entry_time = datetime.utcnow().strftime('%H:%M:%S')
        self.no_md_entries = [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1815,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18151,
                    "MDEntrySize": 1000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 1,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.1813,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18165,
                    "MDEntrySize": 5000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 2,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.181,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18186,
                    "MDEntrySize": 10000000,
                    "MDQuoteType": 1,
                    "MDEntryPositionNo": 3,
                    "SettlDate": self.settle_date_spot,
                    "MDEntryDate": self.md_entry_date,
                    "MDEntryTime": self.md_entry_time
                }
            ]
        self.md_eur_usd_spo = "EUR/USD:SPO:REG:HSBC"
        self.md_entry_px_0 = "1.1815"
        self.md_entry_px_1 = "1.18151"
        self.md_entry_px_2 = "1.1813"
        self.md_entry_px_3 = "1.18165"
        self.md_entry_px_4 = "1.181"
        self.md_entry_px_5 = "1.18186"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_client_tier.find_all_client_tier()
        self.msg_prams_client = self.rest_manager.send_get_request(self.modify_client_tier)
        self.msg_prams_client = self.rest_manager.parse_response_details(self.msg_prams_client,
                                                                         {"clientTierID": self.client_id_silver})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams_client) \
            .change_params({'pricingMethod': "DIR"})
        self.rest_manager.send_post_request(self.modify_client_tier)
        # endregion
        # region Step 2, 4
        self.fix_md.set_market_data().update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion
        # region Step 3
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=self.md_entry_px_0)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=self.md_entry_px_1)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=self.md_entry_px_2)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=self.md_entry_px_3)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryPx=self.md_entry_px_4)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryPx=self.md_entry_px_5)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion
        # region Step 5
        self.md_request.set_md_req_parameters_maker().change_parameters(
            {"SenderSubID": self.silver, "BookType": self.book_type_tiered})
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)

        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "*"])
        self.md_snapshot.get_parameter("NoMDEntries").pop(7)
        self.md_snapshot.get_parameter("NoMDEntries").pop(6)
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
        # "SettlType", "MDEntryPx", "MDEntryTime",
        # "MDQuoteType", "MDOriginType", "MDEntryID",
        # "MDEntrySize","QuoteEntryID", "MDEntryDate"))
        # self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
        # "SettlType", "MDEntryPx", "MDEntryTime",
        # "MDQuoteType", "MDOriginType", "MDEntryID",
        # "MDEntrySize", "QuoteEntryID", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # region Step 6
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams_client) \
            .change_params({'pricingMethod': "VWP"})
        self.rest_manager.send_post_request(self.modify_client_tier)
        # endregion
        self.fix_md.set_market_data().update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
