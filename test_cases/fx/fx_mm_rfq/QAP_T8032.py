from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
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


class QAP_T8032(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fxfh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_buy = FixManager(self.fxfh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_request_prepare = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1")
        self.quote = FixMessageQuoteFX()
        self.order = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_req_id = "USD:FXF:WK1:D3"
        self.bid_price = "0.04"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request_prepare.set_deposit_and_loan_param()
        self.quote_request_prepare.update_repeating_group_by_index("NoRelatedSym", index=0,
                                                                   SettlDate=self.settle_date_spot,
                                                                   MaturityDate=self.settle_date_wk1)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request_prepare, self.test_id)
        # region Send MD for WK1 USD
        self.fix_md.set_md_for_deposit_and_loan_fwd()
        self.fix_md.update_MDReqID(self.md_req_id, self.fxfh_connectivity, "FX")
        self.fix_manager_buy.send_message(self.fix_md)

        # endregion
        # region Step 1
        self.quote_request.set_deposit_and_loan_param()
        self.quote_request.update_repeating_group_by_index("NoRelatedSym", index=0, SettlDate=self.settle_date_spot,
                                                           MaturityDate=self.settle_date_wk1)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        expected_price = str(float(self.bid_price) * 100)[:-2]
        # endregion
        # region Step 3
        self.quote.set_params_for_deposit_and_loan(self.quote_request)
        self.quote.change_parameter("BidPx", str(expected_price))
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.order.set_default_deposit_and_loan(self.quote_request, response[0])
        self.fix_manager_sel.send_message_and_receive_response(self.order)
        # endregion
        # region Step 5
        self.execution_report.set_params_from_deposit_and_loan(self.order)
        self.execution_report.change_parameters({"LastPx": self.bid_price, "AvgPx": expected_price})
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion
