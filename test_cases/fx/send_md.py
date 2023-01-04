import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_MD(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        # self.fx_fh_connectivity = "fix-fh-309-kratos"
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name('client_mm_4')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_2')
        self.security_type = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.no_related_symbols_eur_usd = [{
            'Instrument': {
                'Symbol': "EUR/USD",
                'SecurityType': self.security_type,
                'Product': '4', },
            'SettlType': '0', }]
        self.bands_eur_usd = ["2000000", '6000000', '12000000']


        self.no_md_entries_spot = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1814,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": self.settle_date_spot,
            "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
            }]
        self.no_md_entries_spot_1 = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1813,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": self.settle_date_spot,
            "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
            }]
        self.no_md_entries_spot_2 = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1814,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": self.settle_date_spot,
            "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
            }]
        self.no_md_entries_spot_3 = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1813,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": self.settle_date_spot,
            "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:53:13"
            }]
        self.no_md_entries_spot_4 = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1815,
            "MDEntrySize": 1000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 1,
            "SettlDate": self.settle_date_spot,
            "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:57:13"
        },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": "14:57:13"
            }]

        self.md_req_id = "EUR/USD:FXF:WK2:HSBC"
        # self.md_req_id = "EUR/USD:SPO:REG:HSBC"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-3
        self.fix_md.set_market_data_fwd()
        # # self.fix_md.change_parameter("MDReqID", self.md_req_id)
        # # self.fix_md.set_market_data_fwd()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_1)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_2)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_3)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_1)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_2)
        # self.fix_manager_fh_314.send_message(self.fix_md)
        # self.sleep(1)
        # self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot_3)
        # self.fix_manager_fh_314.send_message(self.fix_md)
