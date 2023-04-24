from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
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
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager


class QAP_T7857(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.expected_notes = "request exceeds quantity threshold for instrument over this client tier"
        self.expected_quoting = "Y"
        self.md_req_id_sp = "EUR/USD:SPO:REG:HSBC"
        self.qty = 4000000
        self.no_side = ""
        self.key_parameter = "quoterequestid"
        self.quote_state = "unavailablepricestate"
        self.quote_state_cause = "unavailablepricecause"
        self.response = None
        self.quote_cancel = FixMessageQuoteCancelFX()

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
            },
            {"MDEntryType": "0",
             "MDEntryPx": 1.1814,
             "MDEntrySize": 2000000,
             "MDQuoteType": 1,
             "MDEntryPositionNo": 2,
             "SettlDate": self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
             },
            {
            "MDEntryType": "1",
            "MDEntryPx": 1.18152,
            "MDEntrySize": 3000000,
            "MDQuoteType": 1,
            "MDEntryPositionNo": 2,
            "SettlDate": self.settle_date_spot,
            "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id_sp, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           OrderQty=self.qty, Currency=self.usd)
        self.response = self.fix_manager_sel.send_message(self.quote_request)
        # region Step 3
        req_id = check_quote_request_id(self.quote_request)
        quote_status = check_quote_status(req_id, self.key_parameter, self.quote_state)
        quote_status_reason = check_quote_status(req_id, self.key_parameter, self.quote_state_cause)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("CCY2, Side Buy")
        self.verifier.compare_values("QuoteStatus", "UNA", quote_status)
        self.verifier.compare_values("QuoteStatusReason", "SPM", quote_status_reason)
        self.verifier.verify()
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           OrderQty=self.qty, Side="2", Currency=self.usd)
        self.response = self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        # region Step 3
        req_id = check_quote_request_id(self.quote_request)
        quote_status = check_quote_status(req_id, self.key_parameter, self.quote_state)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("CCY2, Side Sell")
        self.verifier.compare_values("QuoteStatus", None, quote_status)
        self.verifier.verify()
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager_sel.send_message(self.quote_cancel)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           OrderQty=self.qty, Currency=self.usd)
        self.quote_request.get_parameters()["NoRelatedSymbols"][0].pop("Side")
        self.response = self.fix_manager_sel.send_message(self.quote_request)
        # region Step 3
        req_id = check_quote_request_id(self.quote_request)
        quote_status = check_quote_status(req_id, self.key_parameter, self.quote_state)
        quote_status_reason = check_quote_status(req_id, self.key_parameter, self.quote_state_cause)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("CCY2, No Side")
        self.verifier.compare_values("QuoteStatus", "UNA", quote_status)
        self.verifier.compare_values("QuoteStatusReason", "SPM", quote_status_reason)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id_sp, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(2)
