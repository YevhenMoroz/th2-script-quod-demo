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
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T9039(TestCase):
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
        self.eur_aud = self.data_set.get_symbol_by_name('symbol_17')

        self.no_related_symbols = [{"Instrument": {
            "Symbol": self.eur_aud,
            "SecurityType": self.security_type_spot,
            "Product": "4", },
            "SettlType": self.settle_type_spot}]

        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.md_req_id = f"{self.eur_aud}:SPO:REG:{self.hsbc}"
        self.correct_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.18955,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19909,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17900,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19919,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17400,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19998,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17100,
             "MDEntrySize": 24000000,
             "MDEntryPositionNo": 4,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.12100,
             "MDEntrySize": 24000000,
             "MDEntryPositionNo": 4,
             'SettlDate': self.settle_date_spot,
             'MDQuoteType': 0,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        # endregion

        # region Step 3
        self.md_request.set_md_req_parameters_maker().change_parameter("NoRelatedSymbols",
                                                                       self.no_related_symbols).change_parameter(
            "SenderSubID", self.palladium2)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_empty_md_response(self.md_request, ["*", "*", "*", "*"], response=response[0])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
