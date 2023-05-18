import time
from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import check_quote_status, check_quote_request_id
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T5995(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)

        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_bda = self.data_set.get_settle_date_by_name("wk2_ndf")
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.sec_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.key_parameter = "quoterequestid"
        self.quote_state = "quoterequeststatus"
        self.quote_state_cause = "unavailablepricecause"
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.instrument_swap = {"Symbol": self.eur_usd,
                                "SecurityType": self.sec_type_swap}
        self.instrument_fwd = {"Symbol": self.eur_usd,
                               "SecurityType": self.sec_type_fwd}
        self.md_req_id = f"{self.eur_usd}:FXF:WK1:{self.hsbc}"

        self.correct_no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "SettlDate": self.settle_date_1w,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "SettlDate": self.settle_date_1w,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }, ]

        self.incorrect_no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "SettlDate": self.settle_date_bda,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "SettlDate": self.settle_date_bda,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium1)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # region Step 1
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_fwd)
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_fwd)
        self.fix_md.update_repeating_group("NoMDEntries", self.incorrect_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        time.sleep(4)
        req_id = check_quote_request_id(self.quote_request)
        quote_status = check_quote_status(req_id, self.key_parameter, self.quote_state, "quoterequest")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Quote Cancel presence check")
        self.verifier.compare_values("QuoteStatusReason", "TER", quote_status)
        self.verifier.verify()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data_fwd()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_fwd)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
