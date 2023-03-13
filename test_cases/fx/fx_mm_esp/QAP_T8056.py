import time
from pathlib import Path
from datetime import datetime
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


class QAP_T8056(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_esp_connectivity = self.fix_env.sell_side_esp

        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_esp_connectivity, self.test_id)
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)

        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.settle_type_fwd = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_fwd = self.data_set.get_settle_date_by_name("wk1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.hsbc = "HSBC"
        self.gbp_usd_spot = {"Symbol": self.gbp_usd,
                             "SecurityType": self.sec_type_spot}
        self.no_related_symbols_spot = [{
            "Instrument": {
                "Symbol": self.gbp_usd,
                "SecurityType": self.sec_type_spot,
                "Product": "4", },
            "SettlType": self.settle_type_spot, }]
        self.md_req_id_spot = f"{self.gbp_usd}:SPO:REG:{self.hsbc}"
        self.gbp_usd_fwd = {"Symbol": self.gbp_usd,
                            "SecurityType": self.sec_type_fwd}
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.gbp_usd,
                "SecurityType": self.sec_type_fwd,
                "Product": "4", },
            "SettlType": self.settle_type_fwd, }]
        self.md_req_id = f"{self.gbp_usd}:FXF:WK1:{self.hsbc}"

        self.initial_bid = "1.19996"
        self.initial_ask = "1.19998"

        self.correct_no_md_entries_spot = [
            {"MDEntryType": "0",
             "MDEntryPx": self.initial_bid,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": self.initial_ask,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.correct_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": self.initial_bid,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_fwd,
             "MDEntryForwardPoints": "0.0000001",
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": self.initial_ask,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_fwd,
             "MDEntryForwardPoints": "0.0000001",
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]
        # region incorrect
        self.incorrect_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.1816,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.18168,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.md_request.set_md_req_parameters_maker(). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id_spot, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.md_request.set_md_req_parameters_maker(). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_fwd)
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        self.md_request.set_md_req_parameters_maker(). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx="1.1999601")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx="1.1999801")
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request, "Unsubscribe")
        # endregion
        # region Step 3-4
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_fwd)
        self.fix_md.update_repeating_group("NoMDEntries", self.incorrect_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)

        self.md_request.set_md_req_parameters_maker(). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_empty_md_response(self.md_request, ["*"])
        self.fix_verifier.check_fix_message(self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request, "Unsubscribe")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_fwd)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_spot)
        self.fix_md.update_MDReqID(self.md_req_id_spot, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
