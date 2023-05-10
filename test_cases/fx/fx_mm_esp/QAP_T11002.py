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


class QAP_T11002(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_type_spot = self.data_set.get_settle_type_by_name('spot')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.bands_eur_usd = ["*", '*', '*']
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_spot}]
        self.md_eur_usd_spo = "EUR/USD:SPO:REG:HSBC"
        self.no_md_entries_spo = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18138,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18152,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18132,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18170,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18120,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 2
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spo)
        self.fix_md.update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        # endregion

        # region Step 3-4
        self.md_request.set_md_req_parameters_maker()
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd, response=response[0])
        self.md_snapshot.get_parameter("NoMDEntries").pop(5)
        for i in range(5):
            self.md_snapshot.get_parameter("NoMDEntries")[i]["SettlDate"] = self.settle_date_spot
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_eur_usd_spo, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
