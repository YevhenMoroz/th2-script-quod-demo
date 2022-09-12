from datetime import datetime
from pathlib import Path
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import read_median_file
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX


class QAP_T2642(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.feed_handler2, self.test_id)
        self.md_snapshot_db = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_snapshot_ebs = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.verifier = Verifier(self.test_id)
        self.md_req_id_db = "EUR/USD:SPO:REG:DB"
        self.md_req_id_ebs = "EUR/USD:SPO:REG:EBS-CITI"
        self.no_md_db = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19550,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19674,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18517,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19625,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
            ,
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18417,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19632,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            }
        ]
        self.no_md_ebs = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19568,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19679,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18507,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19628,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S"),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18400,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19632,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime("%Y%m%d"),
                "MDEntryTime": datetime.utcnow().strftime("%H:%M:%S")
            },
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_snapshot_db.set_market_data()
        self.md_snapshot_db.update_repeating_group("NoMDEntries", self.no_md_db)
        self.md_snapshot_db.update_MDReqID(self.md_req_id_db, self.fix_env.feed_handler2, "FX")
        self.fix_manager.send_message(self.md_snapshot_db)

        self.md_snapshot_ebs.set_market_data()
        self.md_snapshot_ebs.update_repeating_group("NoMDEntries", self.no_md_ebs)
        self.md_snapshot_ebs.update_MDReqID(self.md_req_id_ebs, self.fix_env.feed_handler2, "FX")
        self.fix_manager.send_message(self.md_snapshot_ebs)
        # endregion
        # region Step 2
        expected_median = "EUR/USD;EXC;;1.185;6000000;1.19629;12000000'"
        self.sleep(10)
        actual_median = read_median_file()[45:]
        self.verifier.set_event_name("Check median file")
        self.verifier.compare_values("Compare medians", expected_median, actual_median)
        self.verifier.verify()
        # endregion
