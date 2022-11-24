import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps

from rule_management import RuleManager, Simulators

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import (
    OrderBookColumns,
    PostTradeStatuses,
    MiddleOfficeColumns,
    AllocationsColumns,
)
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7230(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "10"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {"Side": "2", "OrderQtyData": {"OrderQty": self.qty}, "Account": self.client, "Price": self.price}
            )
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id: str = response[0].get_parameters()["ClOrdID"]
            order_id: str = response[0].get_parameters()["OrderID"]

        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Check ExecutionReports
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {"ReplyReceivedTime": "*", "LastMkt": "*", "Text": "*", "Account": self.venue_client_names}
        )
        self.exec_report.remove_parameters(["SettlCurrency"])
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=['Account', 'SecurityDesc'])
        # endregion

        # region Book order and checking values after it in the Order book
        self.middle_office.set_modify_ticket_details(
            settl_currency="UAH", exchange_rate="2", exchange_rate_calc="Multiply", toggle_recompute=True
        )
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            "Comparing PostTradeStatus after Book",
        )
        # endregion

        # region Checking the values after the Book in the Middle Office
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [
                MiddleOfficeColumns.price.value,
                MiddleOfficeColumns.sts.value,
                MiddleOfficeColumns.match_status.value,
                MiddleOfficeColumns.settl_currency.value,
                MiddleOfficeColumns.gross_amt.value,
                MiddleOfficeColumns.net_amt.value,
                MiddleOfficeColumns.net_price.value,
            ],
            [MiddleOfficeColumns.order_id.value, order_id],
        )
        self.middle_office.compare_values(
            {
                MiddleOfficeColumns.price.value: "20",
                MiddleOfficeColumns.sts.value: "ApprovalPending",
                MiddleOfficeColumns.match_status.value: "Unmatched",
                MiddleOfficeColumns.settl_currency.value: "UAH",
                MiddleOfficeColumns.gross_amt.value: "2,000",
                MiddleOfficeColumns.net_amt.value: "2,000",
                MiddleOfficeColumns.net_price.value: "20",
            },
            values_after_book,
            "Comparing values after Book for block of MiddleOffice",
        )
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}
        ]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Extracting values from Allocations ticket
        extract_settlement_tab_alloc = self.middle_office.extract_values_from_amend_allocation_ticket(
            panels_extraction=[PanelForExtraction.SETTLEMENT],
            block_filter_dict={MiddleOfficeColumns.order_id.value: order_id},
        )
        fields_for_dlt = ("SettlAmount", "SettlDate", "PSET", "PSETBIC")
        expected_alloc_ticket_values = {}
        for d in self.middle_office.split_tab_misk(extract_settlement_tab_alloc):
            expected_alloc_ticket_values.update(d)
            for key in fields_for_dlt:
                expected_alloc_ticket_values.pop(key, None)
        # endregion

        # region Comparing values in Allocations ticket
        self.middle_office.compare_values(
            {
                MiddleOfficeColumns.settl_currency.value: "UAH",
                MiddleOfficeColumns.exchange_rate.value: "1",
                "ExchangeRateCalc": "",
            },
            expected_alloc_ticket_values,
            "Comparing values in Allocations ticket",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
