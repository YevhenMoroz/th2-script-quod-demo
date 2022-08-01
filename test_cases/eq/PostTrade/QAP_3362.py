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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_3362(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity)
        self.qty = '300'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client('client_pt_8')  # MOClient7 Fully manual with one account
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')  # MOClient7_PARIS
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')  # XPAR

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Split Booking
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        split_param_1 = self.order_book.create_split_booking_parameter(split_qty='100')
        split_param_2 = self.order_book.create_split_booking_parameter(split_qty='200')
        self.order_book.split_book([split_param_1, split_param_2])
        # endregion

        # region Mass Approve
        self.middle_office.mass_approve([1, 2])
        # first block
        values_after_approve_first = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value], row_number=2)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched"},
            values_after_approve_first, "Comparing statuses of first order after Approve")

        # second block
        values_after_approve_second = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value], row_number=1)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched", },
            values_after_approve_second, "Comparing statuses of second order after Approve")
        # endregion

        # region Mass Allocate
        self.middle_office.mass_allocate([1, 2])
        # first block
        values_after_allocate_first = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=2)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched",
             MiddleOfficeColumns.summary_status.value: "MatchedAgreed"}, values_after_allocate_first,
            "Comparing statuses of first order after Allocate")

        # second block
        values_after_allocate_second = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=1)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched",
             MiddleOfficeColumns.summary_status.value: "MatchedAgreed"}, values_after_allocate_second,
            "Comparing statuses of second order after Allocate")
        # endregion

        # region Comparing statuses of first block after Mass Allocate in Allocations
        # first allocation
        values_after_mass_allocate_first_alloc = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
            filter_dict_block={MiddleOfficeColumns.qty.value: '100'})
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: "Affirmed", AllocationsColumns.match_status.value: "Matched"},
            values_after_mass_allocate_first_alloc,
            "Comparing statuses of first block after Mass Allocate in Allocations")

        # second allocation
        values_after_mass_allocate_second_alloc = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
            filter_dict_block={MiddleOfficeColumns.qty.value: '200'}, clear_filter_from_block=True)
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: "Affirmed", AllocationsColumns.match_status.value: "Matched"},
            values_after_mass_allocate_second_alloc,
            "Comparing statuses of second block after Mass Allocate in Allocations")
        # endregion

        # region try Unbook order
        self.middle_office.un_book_order(filter=[OrderBookColumns.order_id.value, order_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Checking PostTradeStatus after trying Unbook')
        # endregion

        # region Mass Un-Allocate
        self.middle_office.mass_unallocate([1, 2])
        # first block
        values_after_mass_unallocate_first = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=2)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched",
             MiddleOfficeColumns.summary_status.value: ""}, values_after_mass_unallocate_first,
            "Comparing statuses of first order after Mass Un-Allocate")

        # second block
        values_after_mass_unallocate_second = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=1)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Accepted", MiddleOfficeColumns.match_status.value: "Matched",
             MiddleOfficeColumns.summary_status.value: ""}, values_after_mass_unallocate_second,
            "Comparing statuses of second order after Mass Un-Allocate")
        # endregion

        # region Unbook order
        self.middle_office.un_book_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value},
            'Checking PostTradeStatus after Unbook order')

        # checking first block
        values_after_unbook_first = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=2)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Canceled", MiddleOfficeColumns.match_status.value: "Unmatched"},
            values_after_unbook_first, "Comparing statuses of first order after Unbook")

        # checking second block
        values_after_unbook_second = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], row_number=1)
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: "Canceled", MiddleOfficeColumns.match_status.value: "Unmatched"},
            values_after_unbook_second, "Comparing statuses of second order after Unbook")
        # endregion

        logger.info(f"Case {self.case_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
