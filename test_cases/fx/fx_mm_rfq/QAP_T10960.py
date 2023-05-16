from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import check_quote_request_id, extract_freenotes, check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T10960(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.verifier = Verifier(self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.quote = FixMessageQuoteFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_bda = self.data_set.get_settle_type_by_name("broken")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_wk1_wk2 = self.data_set.get_settle_date_by_name("broken_w1w2")
        self.settle_date_wk2_wk3 = self.data_set.get_settle_date_by_name("broken_w2w3")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.md_req_id_fwd = "GBP/USD:FXF:WK1:HSBC"

        self.no_md_entries_fwd = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 0,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 0,
                "MDEntryForwardPoints": "0.00002",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 0,
                "MDEntryForwardPoints": "0.00003",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 0,
                "MDEntryForwardPoints": "0.00004",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_fwd)
        self.fix_md.update_MDReqID(self.md_req_id_fwd, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion
        # region step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="GBP", Instrument=self.instrument,
                                                           SettlDate=self.settle_date_wk1_wk2,
                                                           SettlType=self.settle_type_bda)
        self.fix_manager_sel.send_message(self.quote_request)
        # endregion
        # region Step 3
        quote_req_id = check_quote_request_id(self.quote_request)
        quote_status = check_value_in_db(quote_req_id, "quoterequestid", "unavailablepricestate")
        reason = check_value_in_db(quote_req_id, "quoterequestid", "unavailablepricecause")
        self.verifier.set_event_name("check quote status and reason")
        self.verifier.compare_values("quote status", "EOF", quote_status)
        self.verifier.compare_values("quote reason", "CUB", reason)
        self.verifier.verify()

        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="GBP", Instrument=self.instrument,
                                                           SettlDate=self.settle_date_wk2_wk3,
                                                           SettlType=self.settle_type_bda)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        self.quote.prepare_params_for_quote(self.quote_request)
        self.quote.change_parameters({"Side": "*", "OfferForwardPoints": "*"})
        self.fix_verifier.check_fix_message(self.quote)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_MDReqID(self.md_req_id_fwd, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd()
        self.sleep(2)
