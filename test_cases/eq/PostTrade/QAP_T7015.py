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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7015(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '200'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO via FIX
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion

        # region Checking Status in OrderBook
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

        # region Execute CO
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region Complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Book order and checking values in the Order book
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Set-up parameters and check Allocation Report
        self.allocation_message.set_default_ready_to_book(self.fix_message)
        self.allocation_message.change_parameters(
            {'tag5120': '*', 'RootSettlCurrAmt': '*'})
        self.allocation_message.remove_parameters(["Account"])
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

        # # region Set-up parameters and check Allocation Report after Allocate
        # pre_alloc_grp: dict = {
        #     'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}}
        # self.fix_message.change_parameters(pre_alloc_grp)
        # self.allocation_message.set_default_preliminary(self.fix_message)
        # self.allocation_message.change_parameters({'NoAllocs': '*'})
        # self.allocation_message.remove_parameters(
        #     ['RootCommTypeClCommBasis', 'NoRootMiscFeesList', 'RootOrClientCommission',
        #      'RootOrClientCommissionCurrency'])
        # self.fix_verifier_dc.check_fix_message_fix_standard(self.allocation_message,
        #                                                     ['AllocType', 'NoOrders', 'Account'])
        # # endregion

        # region Check Confirmation Report
        self.confirmation_message.set_default_confirmation_new(self.fix_message)
        self.confirmation_message.change_parameters(
            {'tag5120': '*', 'AllocAccount': self.alloc_account})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.confirmation_message,
                                                            ['ConfirmTransType', 'NoOrders', 'AllocAccount'])
        # endregion

        # region Comparing SettlCurrFxRate in Allocations
        settl_curr_fx_rate = self.middle_office.extract_allocate_value('Settl Curr Fx Rate')
        self.middle_office.compare_values({'Settl Curr Fx Rate': ''}, settl_curr_fx_rate,
                                          'Comparing SettlCurrFxRate in Allocations')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
