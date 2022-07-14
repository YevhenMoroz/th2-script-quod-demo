import logging
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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_4897(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message1 = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create first CO order via FIX
        self.fix_message1.set_default_care_limit()
        self.fix_message1.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message1)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion

        # region Set-up parameters for ExecutionReports
        self.exec_report.set_default_new(self.fix_message1)
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Check values in OrderBook
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Execute first CO
        self.order_book.manual_execution(qty=str(round(int(self.qty) / 2)))
        self.order_book.manual_execution(qty=str(round(int(self.qty) / 2)))
        exec_id = self.order_book.extract_2lvl_fields(tab=SecondLevelTabs.executions.value,
                                                      column_names=[OrderBookColumns.exec_id.value], rows=[1],
                                                      filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id})
        # endregion

        # region Create second CO order via FIX
        self.fix_message2.set_default_care_limit()
        self.fix_message2.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
        response2 = self.fix_manager.send_message_and_receive_response(self.fix_message2)
        # get Client Order ID and Order ID
        cl_ord_id2 = response2[0].get_parameters()['ClOrdID']
        order_id2 = response2[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion

        # region Set-up parameters for ExecutionReports
        self.exec_report.set_default_new(self.fix_message2)
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id2])
        # endregion

        # region Check values in OrderBook
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Execute second CO
        self.order_book.manual_execution(qty=str(round(int(self.qty) / 2)))
        self.order_book.manual_execution(qty=str(round(int(self.qty) / 2)))
        exec_id2 = self.order_book.extract_2lvl_fields(tab=SecondLevelTabs.executions.value,
                                                       column_names=[OrderBookColumns.exec_id.value], rows=[1],
                                                       filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id2})
        # endregion

        # region Cancel Executions
        self.trades.cancel_execution({OrderBookColumns.exec_id.value: exec_id[0]['ExecID']})
        self.trades.cancel_execution({OrderBookColumns.exec_id.value: exec_id2[0]['ExecID']})
        # endregion

        # region Refresh orders
        self.order_book.refresh_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.refresh_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id2])
        # endregion

        # region Check Executions
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_second_lvl_fields_list(
            expected_fields={'Qty': str(round(int(self.qty) / 2)), 'Active': 'N'}, row_number=1)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id2]).check_second_lvl_fields_list(
            expected_fields={'Qty': str(round(int(self.qty) / 2)), 'Active': 'N'}, row_number=1)
        # endregion

        # region Complete orders
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id2])
        # endregion

        # region Mass Book orders and checking values after it in the Order book
        self.order_book.mass_book([1, 2])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Mass Book of the first order')
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id2])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Mass Book of the second order')
        # endregion

        # region Checking the values after the Mass Book in the Middle Office
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value,
                                                          [MiddleOfficeColumns.order_id.value, order_id])
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.qty.value, MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.qty.value: str(round(int(self.qty) / 2)),
                                           MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                           MiddleOfficeColumns.match_status.value: 'Unmatched'}, values_after_book,
                                          'Comparing values in the MiddleOffice after the Book of the first order')
        block_id2 = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value,
                                                           [MiddleOfficeColumns.order_id.value, order_id2])
        values_after_book2 = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.qty.value, MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value],
            [MiddleOfficeColumns.block_id.value, block_id2[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.qty.value: str(round(int(self.qty) / 2)),
                                           MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                           MiddleOfficeColumns.match_status.value: 'Unmatched'}, values_after_book2,
                                          'Comparing values in the MiddleOffice after the Book of the second order')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
