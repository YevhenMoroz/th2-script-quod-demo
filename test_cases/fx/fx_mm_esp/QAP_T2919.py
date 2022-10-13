from datetime import datetime
from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2919(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)

        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)

        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.usd_jpy = self.data_set.get_symbol_by_name('symbol_5')
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_3w = self.data_set.get_settle_type_by_name("wk3")
        self.instrument_fwd = {
            'Symbol': self.usd_jpy,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument_fwd,
            'SettlType': self.settle_type_3w}]

        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.ms = self.data_set.get_venue_by_name("venue_3")
        self.instrument_spot = {"Symbol": self.usd_jpy,
                                "SecurityType": self.sec_type_spot}
        self.md_req_id = self.usd_jpy + ':SPO:REG:' + self.ms

        self.no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 118.174,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 118.186,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.ask_spot_without_int = 118.186
        self.bid_spot_without_int = 118.174

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        #  subscribing to marketdata in order to be able to set new marketdata for the instrument:
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion

        # region Step 1-3
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)

        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        ask_pts = float(response[-1].get_parameters()["NoMDEntries"][1]["MDEntryForwardPoints"])
        bid_pts = float(response[-1].get_parameters()["NoMDEntries"][0]["MDEntryForwardPoints"])
        expected_ask_px = str(round(float(self.ask_spot_without_int + ask_pts), 5))
        expected_bid_px = str(round(float(self.bid_spot_without_int + bid_pts), 5))
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=expected_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=expected_ask_px)

        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
