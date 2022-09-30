import time
from datetime import datetime
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX

from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from custom import basic_custom_actions as bca


class QAP_T2926(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_gtw = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.symbol = self.data_set.get_symbol_by_name('symbol_synth_6')
        self.tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_wa = self.data_set.get_fx_instr_type_wa('fx_spot')
        self.account = self.data_set.get_client_by_name("client_mm_4")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type,
        }
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.symbol,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
        }]
        self.md_id_gs = f"{self.symbol}:{self.instr_type_wa}:REG:{self.data_set.get_venue_by_name('venue_8')}"
        self.md_id_citi = f"{self.symbol}:{self.instr_type_wa}:REG:{self.data_set.get_venue_by_name('venue_1')}"
        self.md_id_ms = f"{self.symbol}:{self.instr_type_wa}:REG:{self.data_set.get_venue_by_name('venue_3')}"
        self.md_req_id = ''
        self.no_md_entries_usd_chf_gs = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.005,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.016,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.004,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.017,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.003,
                "MDEntrySize": 20000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.018,
                "MDEntrySize": 20000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.no_md_entries_usd_chf_citi = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.008,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.019,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.007,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.020,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.006,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.021,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]
        self.no_md_entries_usd_chf_ms = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.011,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.022,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.010,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.023,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.009,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.024,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.no_md_entries = [
            {
                'SettlType': 0,
                'MDEntryPx': '1.011',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '1000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryPx': '1.016',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '1000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }, {
                'SettlType': 0,
                'MDEntryPx': '1.01',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '5000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 2,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryPx': '1.0176',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '5000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 2,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }, {
                'SettlType': 0,
                'MDEntryPx': '1.009',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '10000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 3,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryPx': '1.018',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '10000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': self.data_set.get_settle_date_by_name('spot'),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 3,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }

        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.fix_md.change_parameter("MDReqID", self.md_id_citi)
        self.fix_md.change_parameter("NoMDEntries", self.no_md_entries_usd_chf_citi)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_citi}")
        time.sleep(3)

        self.fix_md.change_parameter("MDReqID", self.md_id_ms)
        self.fix_md.change_parameter("NoMDEntries", self.no_md_entries_usd_chf_ms)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_ms}")
        time.sleep(3)

        self.fix_md.change_parameter("MDReqID", self.md_id_gs)
        self.fix_md.change_parameter("NoMDEntries", self.no_md_entries_usd_chf_gs)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_gs}")
        time.sleep(3)

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account).change_parameter(
            'NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.md_snapshot.change_parameter("NoMDEntries", self.no_md_entries)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
