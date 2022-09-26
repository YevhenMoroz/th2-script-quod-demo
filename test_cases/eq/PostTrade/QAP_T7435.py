import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns, OrderType, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7435(TestCase):
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
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')  # VETO
        self.username = environment.get_list_fe_environment()[0].user_1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=OrderType.limit.value, account=self.account,
                                            recipient=self.username, partial_desk=True)
        self.order_ticket.set_miscs_tab_details(['BO1', 'BO2', 'BO3', 'BO4', 'BO5'],
                                                ['ABO1', 'ABO2', 'ABO3', 'ABO4', 'ABO5'])
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
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

        # region Book order
        self.middle_office.set_modify_ticket_details(bo_fields=['Changed BO1', 'Changed BO2'])
        self.middle_office.book_order(filter=[OrderBookColumns.order_id.value, order_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value,
             OrderBookColumns.done_for_day.value: 'Yes'}, 'Comparing PostTradeStatus after Book')
        # endregion

        # region Checking the values after the Book in the Middle Office
        bo_fields = ['Bo Field 1', 'Bo Field 2', 'Bo Field 3', 'Bo Field 4', 'Bo Field 5']
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value] + bo_fields,
            [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'ApprovalPending', MiddleOfficeColumns.match_status.value: 'Unmatched',
             'Bo Field 1': 'Changed BO1', 'Bo Field 2': 'Changed BO2', 'Bo Field 3': 'BO3', 'Bo Field 4': 'BO4',
             'Bo Field 5': 'BO5'}, values_after_book,
            'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [{'Alloc BO Field 1': '', 'Alloc BO Field 2': 'Changed ABO2'}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Checking statuses after Allocate in Middle Office
        values_after_allocate = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'Accepted', MiddleOfficeColumns.match_status.value: 'Matched',
             MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'}, values_after_allocate,
            'Checking statuses after Allocate in Middle Office')
        # endregion

        # region Checking Alloc BO Fields in Allocations
        extracted_fields = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value, 'Alloc BO Field 1',
             'Alloc BO Field 2', 'Alloc BO Field 3', 'Alloc BO Field 4', 'Alloc BO Field 5'])
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: 'Affirmed', AllocationsColumns.match_status.value: 'Matched',
             'Alloc BO Field 1': '', 'Alloc BO Field 2': 'Changed ABO2', 'Alloc BO Field 3': 'ABO3',
             'Alloc BO Field 4': 'ABO4', 'Alloc BO Field 5': 'ABO5'},
            extracted_fields, 'Checking Alloc BO Fields in Allocations')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
