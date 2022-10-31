import time
from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2719(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]

        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fix_env.feed_handler, self.test_id)

        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()

        self.bid_md_entry_px = "0.86142"
        self.ask_md_entry_px = "0.86204"

        self.platinum = self.data_set.get_client_by_name("client_mm_11")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_fwd = self.data_set.get_settle_date_by_name("wk1")
        self.eur_nok = self.data_set.get_symbol_by_name("symbol_6")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.nok_sek = self.data_set.get_symbol_by_name("symbol_14")
        self.usd_sek = self.data_set.get_symbol_by_name("symbol_8")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.eur_nok_spot = {"Symbol": self.eur_nok,
                             "SecurityType": self.sec_type_spot}
        self.eur_usd_spot = {"Symbol": self.eur_usd,
                             "SecurityType": self.sec_type_spot}
        self.nok_sek_spot = {"Symbol": self.nok_sek,
                             "SecurityType": self.sec_type_spot}
        self.usd_sek_spot = {"Symbol": self.usd_sek,
                             "SecurityType": self.sec_type_spot}
        self.mdr_eur_nok_spot = {"Symbol": self.eur_nok,
                                 "SecurityType": self.sec_type_spot,
                                 "Product": "4"}
        self.mdr_eur_usd_spot = {"Symbol": self.eur_usd,
                                 "SecurityType": self.sec_type_spot,
                                 "Product": "4"}
        self.mdr_nok_sek_spot = {"Symbol": self.nok_sek,
                                 "SecurityType": self.sec_type_spot,
                                 "Product": "4"}
        self.mdr_usd_sek_spot = {"Symbol": self.usd_sek,
                                 "SecurityType": self.sec_type_spot,
                                 "Product": "4"}
        self.eur_nok_related_symbols = [{"Instrument": self.mdr_eur_nok_spot}]
        self.eur_usd_related_symbols = [{"Instrument": self.mdr_eur_usd_spot}]
        self.nok_sek_related_symbols = [{"Instrument": self.mdr_nok_sek_spot}]
        self.mdr_related_symbols = [{"Instrument": self.mdr_nok_sek_spot, "SettlType": self.settle_type_spot}]
        self.usd_sek_related_symbols = [{"Instrument": self.mdr_usd_sek_spot}]
        self.eur_nok_req_id = f"{self.eur_nok}:SPO:REG:{self.hsbc}"
        self.eur_usd_req_id = f"{self.eur_usd}:SPO:REG:{self.hsbc}"
        self.nok_sek_req_id = f"{self.nok_sek}:SPO:REG:{self.hsbc}"
        self.usd_sek_req_id = f"{self.usd_sek}:SPO:REG:{self.hsbc}"

        self.md_entries_1 = [
            {"MDEntryType": "0",
             "MDEntryPx": 9.39868,
             "MDEntrySize": 3000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 9.3988,
             "MDEntrySize": 3000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 9.39865,
             "MDEntrySize": 8000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 9.39883,
             "MDEntrySize": 8000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 9.39862,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 9.39886,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.md_entries_2 = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.19597,
             "MDEntrySize": 2000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19609,
             "MDEntrySize": 2000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.19594,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19612,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.19591,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19615,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.md_entries_3 = [
            {"MDEntryType": "0",
             "MDEntryPx": 0.5,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.5,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.md_entries_4 = [
            {"MDEntryType": "0",
             "MDEntryPx": 6.771406,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 66.771416,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 6.771401,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 6.771421,
             "MDEntrySize": 6000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 6.771396,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 6.771426,
             "MDEntrySize": 12000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.md_request.set_md_req_parameters_maker().change_parameter(
            "SenderSubID", self.platinum)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.eur_nok_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.eur_nok_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.md_entries_1)
        self.fix_md.update_MDReqID(self.eur_nok_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

        self.md_request.set_md_req_parameters_maker().change_parameter(
            "SenderSubID", self.platinum)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.eur_usd_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.eur_usd_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.md_entries_2)
        self.fix_md.update_MDReqID(self.eur_usd_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

        self.md_request.set_md_req_parameters_maker().change_parameter(
            "SenderSubID", self.platinum)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.nok_sek_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.nok_sek_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.md_entries_3)
        self.fix_md.update_MDReqID(self.nok_sek_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

        self.md_request.set_md_req_parameters_maker().change_parameter(
            "SenderSubID", self.platinum)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.usd_sek_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.usd_sek_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.md_entries_4)
        self.fix_md.update_MDReqID(self.usd_sek_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

        self.md_request.set_md_req_parameters_maker().change_parameter(
            "SenderSubID", self.platinum)
        self.md_request.update_repeating_group("NoRelatedSymbols", self.mdr_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=self.bid_md_entry_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=self.ask_md_entry_px)
        self.fix_verifier.check_fix_message(self.md_snapshot)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.eur_nok_spot)
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.eur_usd_spot)
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.nok_sek_spot)
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.usd_sek_spot)
        self.fix_manager_fh_314.send_message(self.fix_md)
