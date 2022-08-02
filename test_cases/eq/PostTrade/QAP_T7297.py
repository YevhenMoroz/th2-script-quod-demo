import logging
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, MiddleOfficeColumns, \
    OrderType, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7297(TestCase):
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
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')  # VETO
        self.username = environment.get_list_fe_environment()[0].user_1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.settl_date = datetime.strftime(datetime.now() + timedelta(days=2), '%#m/%#d/%Y')
        self.child_order_book = OMSChildOrderBook(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=OrderType.limit.value, recipient=self.username,
                                            partial_desk=True)
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        cl_ord_id = self.order_book.extract_field(OrderBookColumns.cl_ord_id.value)
        # endregion

        # region Check status in OrderBook
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        self.order_book.check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Child Care
        self.settl_date = datetime.strftime(datetime.now() + timedelta(days=3), '%#m/%#d/%Y')
        self.order_ticket.set_order_details(recipient=self.username, partial_desk=True)
        self.order_ticket.set_settlement_details(settl_date=self.settl_date)
        self.order_ticket.child_care(filter_list=[OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Manual execution Child
        self.child_order_book.manual_execution(settl_date=4)
        # endregion

        # region Complete and Book CO order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Checking Settl Date in Middle Office
        self.settl_date = datetime.strftime(datetime.now() + timedelta(days=4), '%#m/%#d/%Y')
        mo_settl_date = self.middle_office.extract_block_field('SettlDate', [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values({'SettlDate': self.settl_date}, mo_settl_date,
                                          'Checking Settl Date in Middle Office')
        # endregion

        # region Approve and Allocate the block
        self.middle_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id])
        # endregion

        # region Checking Settl Date in Allocations
        alloc_settl_date = self.middle_office.extract_allocate_value('SettlDate')
        self.middle_office.compare_values({'SettlDate': self.settl_date}, alloc_settl_date,
                                          'Checking Settl Date in Allocations')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
