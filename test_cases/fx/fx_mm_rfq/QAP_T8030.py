from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
from test_framework.dep_and_loan_formulas_manager import DepAndLoanManager
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


class QAP_T8030(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fxfh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_fh = FixManager(self.fxfh_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.order = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.settle_date_wk2 = self.data_set.get_settle_date_by_name("wk2")
        self.calc_manager = DepAndLoanManager()
        self.iridium = self.data_set.get_client_by_name("client_mm_3")
        self.konstantin = self.data_set.get_client_by_name("client_mm_12")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.settle_type_wk1 = self.data_set.get_settle_type_by_name("wk1")
        self.settle_type_wk2 = self.data_set.get_settle_type_by_name("wk2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.eur_usd_fwd = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols_wk1 = [{
            'Instrument': self.eur_usd_fwd,
            'SettlType': self.settle_type_wk1}]
        self.no_related_symbols_wk2 = [{
            'Instrument': self.eur_usd_fwd,
            'SettlType': self.settle_type_wk2}]
        self.md_req_id_wk1 = "USD:FXF:WK1:D3"
        self.md_req_id_wk2 = "USD:FXF:WK2:D3"
        self.bid_wk1 = 0.003
        self.offer_wk1 = 0.004
        self.bid_wk2 = 0.005
        self.offer_wk2 = 0.006
        self.no_md_entries_wk1 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_wk1,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_wk1,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk1,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }
        ]
        self.no_md_entries_wk2 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_wk2,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk2,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_wk2,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_wk2,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare MD before sending RFQ
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.iridium)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_wk1)
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_wk2)
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # send MD to TOM
        self.md_snapshot.set_md_for_deposit_and_loan_fwd()
        self.md_snapshot.update_repeating_group("NoMDEntries", self.no_md_entries_wk1)
        self.md_snapshot.update_MDReqID(self.md_req_id_wk1, self.fxfh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.md_snapshot)
        # send MD to WK2
        self.md_snapshot.set_md_for_deposit_and_loan_fwd()
        self.md_snapshot.update_repeating_group("NoMDEntries", self.no_md_entries_wk2)
        self.md_snapshot.update_MDReqID(self.md_req_id_wk2, self.fxfh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.md_snapshot)
        # endregion
        # region Step 1
        self.quote_request.set_deposit_and_loan_param()
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        result = self.calc_manager.calc_dep_and_loan_default(self.bid_wk1, self.offer_wk1, self.bid_wk2,
                                                             self.offer_wk2,
                                                             self.settle_date_wk1, self.settle_date_wk2)
        bid_px = str(round(result[0] * 100, 9))
        # endregion
        # region Step 3
        self.quote.set_params_for_deposit_and_loan(self.quote_request)
        self.quote.change_parameter("BidPx", bid_px)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.order.set_default_deposit_and_loan(self.quote_request, response[0])
        self.fix_manager_sel.send_message_and_receive_response(self.order)
        # endregion
        # region Step 5
        self.execution_report.set_params_from_deposit_and_loan(self.order)
        last_px = round(result[0], 9)
        self.execution_report.change_parameters({"AvgPx": bid_px})
        self.execution_report.remove_fields_from_component("Instrument", ["SecurityType"])
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
