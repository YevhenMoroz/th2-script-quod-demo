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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, MiddleOfficeColumns, \
    PostTradeStatuses, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_3344(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '300'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # get Client Order ID and Order ID
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        cl_ord_id = self.order_book.extract_field(OrderBookColumns.cl_ord_id.value)
        # endregion

        # region Accept order
        self.client_inbox.accept_order()
        # endregion

        # region Set-up parameters and check 107=instrument in ExecutionReports
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters({'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1')})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Execute CO
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region Complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Book order and checking PostTradeStatuses in the Order book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value},
            'Comparing PostTradeStatus after Complete')
        # endregion

        # region Book order
        self.middle_office.set_modify_ticket_details(settl_currency='UAH', toggle_recompute=True)
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Set-up parameters and check 107=instrument in AllocationReport
        self.allocation_message.set_default_ready_to_book(self.fix_message)
        self.allocation_message.change_parameters(
            {'RootCommTypeClCommBasis': '*', 'NoRootMiscFeesList': '*', 'tag5120': '*', 'RootOrClientCommission': '*',
             'RootOrClientCommissionCurrency': '*', 'Currency': 'UAH', 'RootSettlCurrency': 'UAH',
             'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'), 'RootSettlCurrAmt': '*'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.allocation_message,
                                                            ['AllocType', 'Account', 'NoOrders'])
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Set-up parameters and check 107=instrument in AllocationReport2
        pre_alloc_grp: dict = {
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}}
        self.fix_message.change_parameters(pre_alloc_grp)
        self.allocation_message.set_default_preliminary(self.fix_message)
        self.allocation_message.change_parameters(
            {'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'), 'NoAllocs': [
                {'IndividualAllocID': '*', 'AllocNetPrice': '*', 'AllocAccount': self.alloc_account,
                 'AllocQty': self.qty, 'AllocInstructionMiscBlock2': '*', 'AllocPrice': '*', 'NoMiscFees': '*',
                 'AllocSettlCurrAmt': '*', 'AllocSettlCurrency': 'UAH', 'SettlCurrAmt': '*', 'SettlCurrency': 'UAH'}],
             'Currency': 'UAH', 'RootSettlCurrency': '*'})
        self.allocation_message.remove_parameters(
            ['RootCommTypeClCommBasis', 'NoRootMiscFeesList', 'RootOrClientCommission',
             'RootOrClientCommissionCurrency'])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.allocation_message,
                                                            ['AllocType', 'Account', 'NoOrders'])
        # endregion

        # region Set-up parameters and check 107=instrument in Confirmation message
        self.confirmation_message.set_default_confirmation_new(self.fix_message)
        self.confirmation_message.change_parameters(
            {'Account': self.client, 'AllocAccount': self.alloc_account, 'AllocInstructionMiscBlock2': '*',
             'tag5120': '*', 'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'), 'NoMiscFees': '*',
             'CommissionData': '*', 'SettlCurrency': 'UAH', 'Currency': 'UAH', 'SettlCurrAmt': '*', })

        self.fix_verifier_dc.check_fix_message_fix_standard(self.confirmation_message,
                                                            ['ConfirmTransType', 'NoOrders', 'AllocAccount'])
        # endregion

        # region Checking values after Allocate in Middle Office
        values_after_allocate = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'Accepted', MiddleOfficeColumns.match_status.value: 'Matched',
             MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'}, values_after_allocate,
            'Checking statuses after Allocate in Middle Office')
        # endregion

        # region Checking values in Allocations
        extracted_fields = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value])
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: 'Affirmed', AllocationsColumns.match_status.value: 'Matched'},
            extracted_fields, 'Checking statuses in Allocations')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
