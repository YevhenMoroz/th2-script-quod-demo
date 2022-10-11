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


class QAP_T2652(TestCase):
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
        self.palladium2 = self.data_set.get_client_by_name("client_mm_5")
        self.gbp_usd = self.data_set.get_symbol_by_name('symbol_2')
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.instrument_fwd = {
            'Symbol': self.gbp_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols_fwd = [{
            'Instrument': self.instrument_fwd,
            'SettlType': self.settle_type_1w}]
        self.md_gbp_usd_spo = "GBP/USD:SPO:REG:HSBC"
        self.no_md_entries_spo = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.35785,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.35791,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.md_gbp_usd_fwd = "GBP/USD:FXF:WK1:HSBC"
        self.no_md_entries_fwd = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 2.18192,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 1.1819,
                "MDEntryForwardPoints": 0.0002,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 2.18220,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 1.1820,
                "MDEntryForwardPoints": 0.0002,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.fwd_pts_offer = 0.00021
        self.fwd_pts_bid = 0.00019

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 3
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spo)
        self.fix_md.update_MDReqID(self.md_gbp_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_fwd)
        self.fix_md.update_MDReqID(self.md_gbp_usd_fwd, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion
        # region Step 5
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium2)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_fwd)

        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints=self.fwd_pts_bid)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints=self.fwd_pts_offer)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.update_MDReqID(self.md_gbp_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.update_MDReqID(self.md_gbp_usd_fwd, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
