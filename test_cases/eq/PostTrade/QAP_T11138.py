import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    SubmitRequestConst, AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11138(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '100'
        self.price = '10'
        self.account = self.data_set.get_account_by_name("client_pt_1_acc_1")
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.order_modification_request = OrderModificationRequest()
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client,
                                                                             "OrdQty": self.qty, "Price": self.price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value][JavaApiFields.OrdID.value]

        self.trade_entry_request.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        net_amt = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]["NetOrdAmt"]
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        # endregion
        # region Step 2 -Book order
        self.allocation_instruction.set_default_book(order_id)
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        fee_amt = "1000"
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "InstrID": instrument_id, 'ExecAllocList': {'ExecAllocBlock': [{
                'ExecQty': self.qty, 'ExecID': exec_id, 'ExecPrice': self.price}]}, 'RootMiscFeesList':
                {'RootMiscFeesBlock': [{'RootMiscFeeType': "REG", 'RootMiscFeeAmt': fee_amt,
                                        'RootMiscFeeCurr': "EUR", 'RootMiscFeeRate': fee_amt,
                                        'RootMiscFeeBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value}]},
        })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        net_amt_book = str(float(net_amt) + float(fee_amt))
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value, "NetMoney": net_amt_book},
            allocation_report, 'Checking that block created (step 3)')
        # endregion
        # region Step 3 - Approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        # endregion

        # region Step 4 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock", {"AllocAccountID": self.account, "AllocQty": self.qty})
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        alloc_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.Side.value: "B"}, alloc_report_message,
            'Checking side (step 5)')
        # endregion
