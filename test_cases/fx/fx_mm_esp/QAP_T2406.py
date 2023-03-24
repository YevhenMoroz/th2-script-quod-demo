import time
from datetime import datetime
from pathlib import Path

from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2406(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_act = Stubs.fix_act
        self.fx_fh_q_connectivity = self.fix_env.feed_handler2
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_q_connectivity, self.test_id)
        self.security_type = self.data_set.get_security_type_by_name('fx_spot')
        self.md_req_id = "EUR/GBP:SPO:REG:EBS-CITI"
        self.no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18137,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18164,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18106,
                "MDEntrySize": 10000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18197,
                "MDEntrySize": 10000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }
        ]
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.set_instrument = {"Symbol": "EUR/GBP",
                               "SecurityType": "FXSPOT"}
        self.get_instrument = {"Symbol": "EUR/GBP",
                               "SecurityType": "FXSPOT",
                               "Product": "4"}
        self.no_related_symbols = [{
            'Instrument': self.get_instrument,
            'SettlType': self.settle_type}]
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.account = self.data_set.get_client_by_name("client_mm_1")

        self.price_bid_3m = "1.18137"
        self.qty_bid_3m = "3000000"
        self.price_ask_3m = "1.18164"
        self.qty_ask_3m = "3000000"
        self.price_bid_1m = "1.18136"
        self.qty_bid_1m = "1000000"
        self.price_ask_1m = "1.18165"
        self.qty_ask_1m = "1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-3
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.set_instrument)
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_q_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion

        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*"])
        time.sleep(4)
        self.md_snapshot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1m,
                                                         MDEntrySize=self.qty_bid_1m, MDEntryPositionNo="2")
        self.md_snapshot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1m,
                                                         MDEntrySize=self.qty_ask_1m, MDEntryPositionNo="2")
        self.md_snapshot.update_repeating_group_by_index('NoMDEntries', 2, MDEntryPx=self.price_bid_3m,
                                                         MDEntrySize=self.qty_bid_3m, MDEntryPositionNo="1")
        self.md_snapshot.update_repeating_group_by_index('NoMDEntries', 3, MDEntryPx=self.price_ask_3m,
                                                         MDEntrySize=self.qty_ask_3m, MDEntryPositionNo="1")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
