import time
from random import randint
from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_quote_request_id, extract_automatic_quoting
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T8586(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.java_quote = OrderQuoteFX()
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.action_request = QuoteRequestActionRequestFX()
        self.quote = FixMessageQuoteFX()
        self.platinum = self.data_set.get_client_by_name("client_mm_11")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")

        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.status_filled = Status.Fill

        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.qty_6m = "6000000"
        self.qty_10m = "10000000"

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.free_notes_column = OrderBookColumns.free_notes.value
        self.qty_column = OrderBookColumns.qty.value
        self.client_column = QuoteRequestBookColumns.client.value
        self.presence_event = "Order presence check"
        self.expected_free_notes = "not enough quantity available through volume bands - manual intervention required"

        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.zar_mxn = self.data_set.get_symbol_by_name("symbol_19")
        self.mxn = self.data_set.get_currency_by_name("currency_mxn")
        self.usd_zar = self.data_set.get_symbol_by_name("symbol_20")
        self.eur_mxn = self.data_set.get_symbol_by_name("symbol_21")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_spot")
        self.choice = randint(1, 2)
        self.instrument_zar_mxn = {"Symbol": self.zar_mxn,
                                   "SecurityType": self.sec_type_spot}
        if self.choice == 1:
            self.instrument_spot = {"Symbol": self.usd_zar,
                                    "SecurityType": self.sec_type_spot}
            self.md_req_id = f"{self.usd_zar}:SPO:REG:{self.hsbc}"
        elif self.choice == 2:
            self.instrument_spot = {"Symbol": self.eur_mxn,
                                    "SecurityType": self.sec_type_spot}
            self.md_req_id = f"{self.eur_mxn}:SPO:REG:{self.hsbc}"

        self.no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.1815,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.18151,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.1813,
             "MDEntrySize": 5000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.1817,
             "MDEntrySize": 5000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
        # endregion
        # region Step 3
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.platinum,
                                                           Currency=self.mxn, Instrument=self.instrument_zar_mxn,
                                                           OrderQty=self.qty_6m, Side="2")
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_fwd_ccy2(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion
        # region Step 4
        self.new_order_single.set_default_prev_quoted_ccy2(self.quote_request, response[0])
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single_ccy2(self.new_order_single, self.status_filled)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
        # region Step 5
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.platinum,
                                                           Currency=self.mxn, Instrument=self.instrument_zar_mxn,
                                                           OrderQty=self.qty_10m, Side="2")
        self.fix_manager.send_message(self.quote_request)
        automatic_quoting = extract_automatic_quoting(self.quote_request)
        self.verifier.set_event_name("Check quote presence in DI")
        self.verifier.compare_values("Check quote presence in DI", "N",  automatic_quoting)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
