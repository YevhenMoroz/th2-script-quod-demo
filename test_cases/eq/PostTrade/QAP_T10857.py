import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10857(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '100'
        self.price = '20'
        self.account = self.data_set.get_account_by_name("client_pt_1_acc_1")
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.unbook_request = BookingCancelRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region step 1

        self.trade_entry_request.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]

        exec_id = execution_report[JavaApiFields.ExecID.value]

        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)

        self.allocation_instruction.set_default_book(order_id)
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"InstrID": instrument_id, 'ExecAllocList': {
                                                                   'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                       'ExecID': exec_id,
                                                                                       'ExecPrice': self.price}]}})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        book_id = self.java_api_manager.get_first_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value][JavaApiFields.ClientAllocID.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value}, allocation_report,
            'Checking that block created (step 1)')
        # endregion

        # region Step 2 - Approve and Allocatr block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)

        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.account,
                "AllocQty": self.qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)

        alloc_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {
                "AllocStatus": AllocationReportConst.AllocStatus_ACK.value,
                "MatchStatus": AllocationReportConst.MatchStatus_MAT.value,
                "AllocSummaryStatus": AllocationReportConst.AllocSummaryStatus_MAG.value,
            }, alloc_report_message, "Allocate block (step 2)")
        # endregion
        # region Step 2 - Unbook order
        self.unbook_request.set_default(book_id)
        self.java_api_manager.send_message_and_receive_response(self.unbook_request)
        unbook_reply = self.java_api_manager.get_last_message(
            ORSMessageType.BookingCancelReply.value).get_parameters()[JavaApiFields.MessageReply.value][JavaApiFields.MessageReplyBlock.value][0]
        self.java_api_manager.compare_values({"ErrorCD":"QUOD-24806"},unbook_reply,"Check unbook")