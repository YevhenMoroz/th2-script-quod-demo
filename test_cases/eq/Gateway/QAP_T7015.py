import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
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
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_co_1')  # MOClient
        self.alloc_account = self.data_set.get_account_by_name('client_co_1_acc_1')  # MOClient_SA1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO via FIX
        class_name = QAP_T7015
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
        response = self.fix_manager.send_message_and_receive_response(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region Execute CO
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager.send_message(self.trade_entry_message)
        # endregion

        # region Complete order
        self.complete_order.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_order)
        # endregion

        # region Book order and checking values in the Order book
        instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        self.allocation_instruction.set_default_book(order_id)
        amount = str(int(self.price) * int(self.qty))
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "GrossTradeAmt": amount,
            'Qty': self.qty,
            'SettlCurrAmt': amount,
            "InstrID": instr_id,
            "AvgPx": self.price,
            "AccountGroupID": self.client
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("Messages after BOOK", responses)
        post_trade_status = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)[JavaApiFields.PostTradeStatus.value]
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {OrderBookColumns.post_trade_status.value: post_trade_status},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Set-up parameters and check Allocation Report
        self.allocation_message.set_default_ready_to_book(self.fix_message)
        self.allocation_message.change_parameters(
            {'tag5120': '*', 'RootSettlCurrAmt': '*','SettlCurrFxRate': '#'})
        self.allocation_message.remove_parameters(["Account"])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.allocation_message,
                                                            ['AllocType', 'Account', 'NoOrders'])
        # endregion

        # region Approve and Allocate block
        alloc_id = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)[JavaApiFields.ClientAllocID.value]
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message('Messages after APPROVE', responses)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.alloc_account,
            'AllocQty': self.qty,
            'AvgPx': self.price,
            "InstrID": instr_id
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message('Messages after ALLOCATE', responses)

        # region Set-up parameters and check Allocation Report after Allocate
        list_of_ignored_fields = ['Account']
        pre_alloc_grp: dict = {
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}}
        self.fix_message.change_parameters(pre_alloc_grp)
        self.allocation_message.set_default_preliminary(self.fix_message)
        self.allocation_message.change_parameters({'NoAllocs': '*', 'SettlCurrFxRate': '#'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.allocation_message,
                                                            ['NoOrders', 'AllocType'],
                                                            ignored_fields=list_of_ignored_fields)
        # endregion

        # region Check Confirmation Report
        self.confirmation_message.set_default_confirmation_new(self.fix_message)
        self.confirmation_message.change_parameters(
            {'tag5120': '*', 'AllocAccount': self.alloc_account,'SettlCurrFxRate': '#'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.confirmation_message,
                                                            ['ConfirmTransType', 'NoOrders', 'AllocAccount'])
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
