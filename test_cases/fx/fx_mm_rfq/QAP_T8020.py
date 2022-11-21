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
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T8020(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fxfh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_fh = FixManager(self.fxfh_connectivity, self.test_id)
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.settle_date_tom = self.data_set.get_settle_date_by_name("tomorrow")
        self.settle_date_wk2 = self.data_set.get_settle_date_by_name("wk2")
        self.quote = FixMessageQuoteFX()
        self.order = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.calc_manager = DepAndLoanManager()
        self.md_req_id_tom = "USD:FXF:TOM:D3"
        self.md_req_id_wk2 = "USD:FXF:WK2:D3"
        self.bid_tom = 0.004
        self.offer_tom = 0.005
        self.bid_wk2 = 0.006
        self.offer_wk2 = 0.007
        self.no_md_entries_tom = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_tom,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_tom,
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_tom,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.00001",
                "SettlDate": self.settle_date_tom,
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
        # send MD to TOM
        self.quote_request.set_deposit_and_loan_param()
        self.quote_request.update_repeating_group_by_index("NoRelatedSym", index=0, SettlDate=self.settle_date_tom,
                                                           MaturityDate=self.settle_date_wk2)
        self.md_snapshot.set_md_for_deposit_and_loan_fwd()
        self.md_snapshot.update_repeating_group("NoMDEntries", self.no_md_entries_tom)
        self.md_snapshot.update_MDReqID(self.md_req_id_tom, self.fxfh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.md_snapshot)
        # send MD to WK2
        self.md_snapshot.set_md_for_deposit_and_loan_fwd()
        self.md_snapshot.update_repeating_group("NoMDEntries", self.no_md_entries_wk2)
        self.md_snapshot.update_MDReqID(self.md_req_id_wk2, self.fxfh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.md_snapshot)
        # endregion
        # region Step 1
        self.quote_request.set_deposit_and_loan_param()
        self.quote_request.update_repeating_group_by_index("NoRelatedSym", index=0, SettlDate=self.settle_date_tom,
                                                           MaturityDate=self.settle_date_wk2)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        result = self.calc_manager.calc_dep_and_loan_before_spot(self.bid_tom, self.offer_tom, self.bid_wk2,
                                                                 self.bid_wk2,
                                                                 self.settle_date_tom, self.settle_date_wk2)
        bid_px = str(result[0] * 100)
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
        self.execution_report.change_parameters({"AvgPx": bid_px, "LastPx": last_px})
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion
