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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, AllocationsColumns, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6965(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty_first = "100"
        self.qty_second = "200"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account_1 = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.alloc_account_2 = self.data_set.get_account_by_name("client_pt_1_acc_2")  # MOClient_SA2
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message_first = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_second = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create first CO via FIX
        self.fix_message_first.set_default_care_limit()
        self.fix_message_first.change_parameters(
            {"Side": "1", "OrderQtyData": {"OrderQty": self.qty_first}, "Account": self.client})
        response_first = self.fix_manager.send_message_and_receive_response(self.fix_message_first)
        # get Client Order ID and Order ID
        cl_ord_id_first = response_first[0].get_parameters()["ClOrdID"]
        order_id_first = response_first[0].get_parameters()["OrderID"]
        self.client_inbox.accept_order()
        # endregion

        # region Create second CO via FIX
        self.fix_message_second.set_default_care_limit()
        self.fix_message_second.change_parameters(
            {"Side": "1", "OrderQtyData": {"OrderQty": self.qty_second}, "Account": self.client})
        response_second = self.fix_manager.send_message_and_receive_response(self.fix_message_second)
        # get Client Order ID and Order ID
        cl_ord_id_second = response_second[0].get_parameters()["ClOrdID"]
        order_id_second = response_second[0].get_parameters()["OrderID"]
        self.client_inbox.accept_order()
        # endregion

        # region Execute Orders
        self.order_book.manual_execution(filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id_first})
        self.order_book.manual_execution(filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id_second})
        # endregion

        # region Complete orders
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id_first])
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id_second])
        # endregion

        # region Mass Book orders and checking PostTradeStatus in the Order book
        self.order_book.mass_book([1, 2])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_first])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            "Comparing PostTradeStatus after Mass Book of the first order")
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_second])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            "Comparing PostTradeStatus after Mass Book of the second order")
        # endregion

        # region Approve orders and checking values in the MO
        self.middle_office.mass_approve([1, 2])
        # first block
        values_after_approve_first = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.conf_service.value, MiddleOfficeColumns.sts.value,
             MiddleOfficeColumns.match_status.value], [MiddleOfficeColumns.order_id.value, order_id_first])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.conf_service.value: "Manual", MiddleOfficeColumns.sts.value: "Accepted",
             MiddleOfficeColumns.match_status.value: "Matched"}, values_after_approve_first,
            "Comparing values of first order after Approve")

        # second block
        values_after_approve_second = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.conf_service.value, MiddleOfficeColumns.sts.value,
             MiddleOfficeColumns.match_status.value], [MiddleOfficeColumns.order_id.value, order_id_second])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.conf_service.value: "Manual", MiddleOfficeColumns.sts.value: "Accepted",
             MiddleOfficeColumns.match_status.value: "Matched", }, values_after_approve_second,
            "Comparing values of second order after Approve")
        # endregion

        # region Allocate first block
        allocation_param = [{AllocationsColumns.security_acc.value: self.alloc_account_1,
                             AllocationsColumns.alloc_qty.value: self.qty_first}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id_first])
        # endregion

        # region Allocate second block
        allocation_param = [{AllocationsColumns.security_acc.value: self.alloc_account_2,
                             AllocationsColumns.alloc_qty.value: self.qty_second}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param, clear_filter=True)
        self.middle_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id_second])
        # endregion

        # region Mass Un-Allocate blocks
        self.middle_office.mass_unallocate([1, 2])
        # endregion

        # region Comparing values of first block after Mass Un-Allocate in MO
        # first block
        values_after_mass_un_allocate_first_mo = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.conf_service.value, MiddleOfficeColumns.sts.value,
             MiddleOfficeColumns.match_status.value], [MiddleOfficeColumns.order_id.value, order_id_first])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.conf_service.value: "Manual", MiddleOfficeColumns.sts.value: "Accepted",
             MiddleOfficeColumns.match_status.value: "Matched"}, values_after_mass_un_allocate_first_mo,
            "Comparing values of first block after Mass Un-Allocate in MO")

        # second block
        values_after_mass_un_allocate_second_mo = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.conf_service.value, MiddleOfficeColumns.sts.value,
             MiddleOfficeColumns.match_status.value], [MiddleOfficeColumns.order_id.value, order_id_first])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.conf_service.value: "Manual", MiddleOfficeColumns.sts.value: "Accepted",
             MiddleOfficeColumns.match_status.value: "Matched"}, values_after_mass_un_allocate_second_mo,
            "Comparing values of second block after Mass Un-Allocate in MO")
        # endregion

        # region Comparing statuses of first block after Mass Un-Allocate in Allocations
        # first allocation
        values_after_mass_un_allocate_first_alloc = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
            filter_dict_block={MiddleOfficeColumns.order_id.value: order_id_first})
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: "Canceled", MiddleOfficeColumns.match_status.value: "Unmatched"},
            values_after_mass_un_allocate_first_alloc,
            "Comparing statuses of first block after Mass Un-Allocate in Allocations")

        # second allocation
        values_after_mass_un_allocate_second_alloc = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
            filter_dict_block={MiddleOfficeColumns.order_id.value: order_id_second})
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: "Canceled", MiddleOfficeColumns.match_status.value: "Unmatched"},
            values_after_mass_un_allocate_second_alloc,
            "Comparing statuses of second block after Mass Un-Allocate in Allocations")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
