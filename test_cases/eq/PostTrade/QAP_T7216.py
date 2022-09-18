import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns, TimeInForce, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7216(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.desk = environment.get_list_fe_environment()[0].desk_2
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_3')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')  # VETO
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=OrderType.limit.value, tif=TimeInForce.DAY.value,
                                            washbook=self.washbook, recipient=self.desk)
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        cl_ord_id = self.order_book.extract_field(OrderBookColumns.cl_ord_id.value)
        # endregion

        # region Accept CO order
        self.client_inbox.accept_order()
        # endregion

        # region Check status in OrderBook
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Execute CO
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region Complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Check values in OrderBook after Complete
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after Complete')
        # endregion

        # region Book order
        self.middle_office.book_order(filter=[OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Checking values after the Book in the Middle Office
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value,
                                                          [MiddleOfficeColumns.order_id.value, order_id])
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value, 'WashBookAccount'],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                           MiddleOfficeColumns.match_status.value: 'Unmatched',
                                           'WashBookAccount': self.washbook}, values_after_book,
                                          'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Approve and Allocate the block
        self.middle_office.approve_block()
        allocation_param = [
            {'Security Account': self.data_set.get_account_by_name('client_pt_1_acc_1'), 'Alloc Qty': self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Verifying WashBookAccountID after Allocate
        washbook_from_alloc = self.middle_office.extract_allocate_value(column_name='WashBookAccountID ')
        self.middle_office.compare_values({'WashBookAccountID ': self.washbook}, washbook_from_alloc,
                                          'Comparing WashBookAccount after Allocate')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
