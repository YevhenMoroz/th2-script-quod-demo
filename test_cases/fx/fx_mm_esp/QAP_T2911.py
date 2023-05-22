from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from decimal import Decimal

class QAP_T2911(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.verifier = Verifier(self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.instrument_spot = {
            'Symbol': self.gbp_usd,
            'SecurityType': self.sec_type_spot,
            'Product': '4'}
        self.no_related_symbols_spot = [{
            'Instrument': self.instrument_spot,
            'SettlType': self.settle_type_spot}]

        self.gbp_usd_spot = {"Symbol": self.gbp_usd,
                             "SecurityType": self.sec_type_spot}
        self.md_req_id = f"{self.gbp_usd}:SPO:REG:{self.hsbc}"

        self.bid_px = Decimal(1.18150)
        self.ask_px = Decimal(1.1825)
        self.new_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": str(self.bid_px),
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": str(self.ask_px),
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.expected_effective_bid_margin = "-4.0"
        self.expected_effective_ask_margin = "-4.0"
        self.bid_test = "bid effective margin"
        self.ask_test = "ask effective margin"
        self.test = "Verify effective margins"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.new_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        effected_bid_px = Decimal(response[0].get_parameter("NoMDEntries")[0]["MDEntryPx"])
        effected_ask_px = Decimal(response[0].get_parameter("NoMDEntries")[1]["MDEntryPx"])
        actual_effective_bid_margin = str(round((self.bid_px - effected_bid_px) * 10000, 1))
        actual_effective_ask_margin = str(round((effected_ask_px - self.ask_px) * 10000, 1))
        # region 3-4
        self.verifier.set_event_name(self.test)
        self.verifier.compare_values(self.bid_test, self.expected_effective_bid_margin, actual_effective_bid_margin)
        self.verifier.compare_values(self.ask_test, self.expected_effective_ask_margin, actual_effective_ask_margin)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.gbp_usd_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
