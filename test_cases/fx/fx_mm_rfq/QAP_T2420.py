from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2420(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.status = Status.Fill
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.quote = FixMessageQuoteFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.qty = "51000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_esp = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.gbp_usd_spot = {
            'Symbol': self.symbol,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.gbp_usd_spot,
            'SettlType': self.settle_type_spot}]
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.gbp_usd_fwd = {
            'Symbol': self.symbol,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols_fwd = [{
            'Instrument': self.gbp_usd_fwd,
            'SettlType': self.settle_type_wk1}]
        self.md_req_id_sp = "GBP/USD:SPO:REG:HSBC"
        self.md_req_id_fwd = "GBP/USD:FXF:WK1:HSBC"

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
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00002",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00003",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 50000000,
                "MDEntryPositionNo": 2,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00004",
                "SettlDate": self.settle_date_wk1,
                "MDEntryTime": datetime.utcnow().strftime("%Y%m%d"),
            }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_esp.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_esp.send_message(self.md_request)
        self.fix_md.set_market_data().update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_req_id_sp, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_fwd)
        self.fix_manager_esp.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_esp.send_message(self.md_request)
        self.fix_md.set_market_data_fwd().update_repeating_group("NoMDEntries", self.no_md_entries_fwd)
        self.fix_md.update_MDReqID(self.md_req_id_fwd, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion
        # region step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_qty=self.qty, leg_symbol=self.symbol)
        self.quote_request.update_far_leg(leg_qty=self.qty, leg_symbol=self.symbol)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="GBP", Instrument=self.instrument)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 3
        self.new_order_single.set_default_prev_quoted_swap(self.quote_request, response[0])
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_swap(self.new_order_single, self.status)
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
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
