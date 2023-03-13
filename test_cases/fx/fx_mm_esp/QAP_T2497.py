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


class QAP_T2497(TestCase):
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
                "MDEntryPx": 1.18126,
                "MDEntrySize": 10000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18177,
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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*"], response=response[0])
        self.md_snapshot.change_parameter("OrigQuoteEntryID", "*")
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
