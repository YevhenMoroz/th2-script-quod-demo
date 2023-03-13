from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import extract_freenotes
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2417(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixQuoteRequestFX()
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.expected_notes = "request exceeds quantity threshold for instrument over this client tier"
        self.expected_quoting = "N"
        self.qty = "51000000"
        self.md_req_id_sp = "EUR/USD:SPO:REG:HSBC"
        self.md_req_id_fwd = "EUR/USD:FXF:WK1:HSBC"

        self.no_md_entries_spot = [{
            "MDEntryType": "0",
            "MDEntryPx": 1.1815,
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
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }]
        self.no_md_entries_fwd = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1814,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18164,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 1,
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 1,
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id_sp, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_fwd)
        self.fix_md.update_MDReqID(self.md_req_id_fwd, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params_swap()
        self.quote_request.update_near_leg(leg_qty=self.qty)
        self.quote_request.update_far_leg(leg_qty=self.qty)
        response: list = self.java_api_manager.send_message_and_receive_response(self.quote_request)
        # region Step 3
        received_notes = response[0].get_parameter("QuoteRequestNotifBlock")["FreeNotes"]
        received_quoting = response[0].get_parameter("QuoteRequestNotifBlock")["AutomaticQuoting"]
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check FreeNotes and AutomaticQuoting")
        self.verifier.compare_values("Free notes", self.expected_notes, received_notes)
        self.verifier.compare_values("AutomaticQuoting", self.expected_quoting, received_quoting)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_sp, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_MDReqID(self.md_req_id_fwd, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(2)
