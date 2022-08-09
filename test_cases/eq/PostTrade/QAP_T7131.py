import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, MiddleOfficeColumns, \
    PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7131(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.price = '1.12345678'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_3')  # MOClient3
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region Accept order
        self.client_inbox.accept_order()
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Checking Status in OrderBook
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Execute first CO
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region Check ExecSts after Execution
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion

        # region Complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Book order and checking PostTradeStatuses in the Order book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Checking the Price in the Middle Office
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.price.value, MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value],
            [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values({MiddleOfficeColumns.price.value: '1.124',
                                           MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                           MiddleOfficeColumns.match_status.value: 'Unmatched'}, values_after_book,
                                          'Comparing values in the MiddleOffice after the Book of the first order')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
