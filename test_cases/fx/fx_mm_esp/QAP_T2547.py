import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T2547(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]

        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.adm_env.session_alias_wa, self.test_id)
        self.modify_client_tier = RestApiClientTierMessages()
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.palladium2_id = self.data_set.get_client_tier_id_by_name("client_tier_id_5")
        self.palladium2 = self.data_set.get_client_by_name("client_mm_5")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.eur_gbp = self.data_set.get_symbol_by_name('symbol_3')
        self.aud_usd = self.data_set.get_symbol_by_name('symbol_16')
        self.gbp_usd = self.data_set.get_symbol_by_name('symbol_2')

        self.no_related_symbols_1 = [{"Instrument": {
            "Symbol": self.eur_usd,
            "SecurityType": self.security_type_spot,
            "Product": "4", },
            "SettlType": self.settle_type_spot}]
        self.no_related_symbols_2 = [{"Instrument": {
            "Symbol": self.eur_gbp,
            "SecurityType": self.security_type_spot,
            "Product": "4", },
            "SettlType": self.settle_type_spot}]
        self.no_related_symbols_3 = [{"Instrument": {
            "Symbol": self.aud_usd,
            "SecurityType": self.security_type_spot,
            "Product": "4", },
            "SettlType": self.settle_type_spot}]
        self.no_related_symbols_4 = [{"Instrument": {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_spot,
            "Product": "4", },
            "SettlType": self.settle_type_spot}]

        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.md_req_id_1 = f"{self.eur_usd}:SPO:REG:{self.hsbc}"
        self.md_req_id_2 = f"{self.eur_gbp}:SPO:REG:{self.hsbc}"
        self.md_req_id_3 = f"{self.aud_usd}:SPO:REG:{self.hsbc}"
        self.md_req_id_4 = f"{self.gbp_usd}:SPO:REG:{self.hsbc}"
        self.bid_1 = 1.18955
        self.bid_2 = 1.17900
        self.bid_3 = 1.17400
        self.ask_1 = 1.19909
        self.ask_2 = 1.19919
        self.ask_3 = 1.19998
        self.correct_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.18955,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19909,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17900,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19919,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17400,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19998,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},

        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_client_tier.find_client_tier(self.palladium2_id)
        self.msg_prams = self.rest_manager.send_get_request_filtered(self.modify_client_tier)
        self.msg_prams = self.rest_manager.parse_response_details(self.msg_prams, {"clientTierID": self.palladium2_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams) \
            .change_params({'pricingMethod': "DIR"})
        self.rest_manager.send_post_request(self.modify_client_tier)
        # endregion

        # region Step 2
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id_1, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_2, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_3, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_4, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        # endregion

        # region Step 3
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols_1).change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["1000000", "*", "*"], priced=False,
                                                    band_not_priced=["1000000", "prc", "prc"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=round(self.bid_2 - 0.00002, 5))
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=round(self.ask_2 + 0.00002, 5))
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 4
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols_2).change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=1.18410)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=1.19909)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 5
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols_2).change_parameter(
            "BookType", "1").change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "*"], response=response[0])
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

        # region Step 6
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols_3).change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*", "*"], response=response[0])
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 6, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.md_snapshot.remove_values_in_repeating_group_by_index("NoMDEntries", 7, (
            "SettlType", "MDEntryTime", "MDEntryPx", "MDQuoteType", "MDOriginType", "MDEntryID",
            "QuoteEntryID", "MDEntrySize", "MDEntryDate"))
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region Step 7
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols_4).change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["1000000", "*", "*"], published=False,
                                                    band_not_pub=["1000000", "pub", "pub"], response=response[0])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_1, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_2, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_3, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_req_id_4, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.modify_client_tier.modify_client_tier().set_params(self.msg_prams) \
            .change_params({'pricingMethod': "VWP"})
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.sleep(2)
