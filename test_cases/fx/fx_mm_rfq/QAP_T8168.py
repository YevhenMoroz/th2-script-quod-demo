import copy
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T8168(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rqf_connectivity = self.fix_env.sell_side_rfq
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_manager_gtw = FixManager(self.rqf_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.rqf_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fx_fh_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_request_2 = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_esp = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_2 = FixMessageQuoteFX()
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.new_order_single_2 = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_15")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date = self.data_set.get_settle_date_by_name("spot")
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.instrument_2 = copy.deepcopy(self.instrument)
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.usd_nok_spot = {
            'Symbol': self.symbol,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.usd_nok_spot,
            'SettlType': self.settle_type_spot}]
        self.md_req_id = "USD/NOK:SPO:REG:HSBC"
        self.no_md_entries_spot = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 6000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }
        ]
        self.qty = "6000000"
        self.side_sell = "1"
        self.qty2 = "5000000"
        self.side_buy = "2"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Prepare MD
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.client)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_esp.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_esp.send_message(self.md_request)
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion

        # region Step 3
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           Instrument=self.instrument,
                                                           Account=self.client, Currency=self.currency,
                                                           OrderQty=self.qty, Side=self.side_sell)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_fwd(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

        # region Step 5
        self.quote_request_2.set_rfq_params_fwd()
        self.quote_request_2.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                             Instrument=self.instrument_2,
                                                             Account=self.client, Currency=self.currency,
                                                             OrderQty=self.qty2, Side=self.side_buy)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request_2, self.test_id)
        self.quote_2.set_params_for_quote_fwd(self.quote_request_2)
        self.fix_verifier.check_fix_message(self.quote_2)
        # endregion
        # region Step 6
        self.new_order_single_2.set_default_prev_quoted(self.quote_request_2, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single_2)
        self.execution_report.set_params_from_new_order_single(self.new_order_single_2)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.sleep(2)
