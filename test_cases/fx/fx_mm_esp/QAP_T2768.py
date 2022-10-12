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


class QAP_T2768(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.palladium2 = self.data_set.get_client_by_name("client_mm_5")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_type_1m = self.data_set.get_settle_type_by_name('m1')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.bid_fwd_pts = '-0.0000099'
        self.offer_fwd_pts = '0.0000101'
        self.bands_eur_usd = ["*", '*', '*']
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_1m}]
        self.md_eur_usd_spo = "EUR/USD:SPO:REG:HSBC"
        self.no_md_entries_spo = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19597,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19609,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19594,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19612,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19591,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19615,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.md_eur_usd_fwd = "EUR/USD:FXF:MO1:HSBC"
        self.no_md_entries_fwd = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19585,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0000001',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19615,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0000001',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        #  !subscribing to MD in order to modify it!
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium2)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 2
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spo)
        self.fix_md.update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_fwd)
        self.fix_md.update_MDReqID(self.md_eur_usd_fwd, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion

        # region Step 3-4
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.palladium2)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints=self.bid_fwd_pts,
                                                         SettlDate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints=self.offer_fwd_pts,
                                                         SettlDate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints=self.bid_fwd_pts,
                                                         SettlDate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints=self.offer_fwd_pts,
                                                         SettlDate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints=self.bid_fwd_pts,
                                                         SettlDate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints=self.offer_fwd_pts,
                                                         SettlDate="*")
        self.sleep(4)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_MDReqID(self.md_eur_usd_fwd, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
