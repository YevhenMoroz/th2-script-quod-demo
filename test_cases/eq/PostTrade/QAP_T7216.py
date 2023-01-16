import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


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
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order (step 1)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            "ClOrdID": bca.client_orderid(9),
            'Price': self.price,
            'WashBookAccountID': self.washbook
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create CO order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region trade CO order and complete it (step 2)
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.venue})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        print_message(f'Trade CO  order {order_id}', responses)
        response = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = response[JavaApiFields.ExecID.value]
        self.complete_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        print_message(f'Complete CO  order {order_id}', responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, order_reply,
            f'Check {JavaApiFields.PostTradeStatus.value} (step 2)')
        # endregion

        # region book CO order (step 3)
        gross_trade_amt = str(float(self.qty) * float(self.price))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "AccountGroupID": self.client,
            "SettlCurrAmt": gross_trade_amt,
            'Qty': self.qty,
            'ExecAllocList': {
                'ExecAllocBlock': [{'ExecQty': self.qty,
                                    'ExecID': exec_id,
                                    'ExecPrice': self.price}]},
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message(f'Book {order_id} order', responses)
        allocation_report = \
        self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.WashBookAccountID.value: self.washbook
             }, allocation_report, 'Check expected and actually result from step 3')
        # endregion

        # region Approve and Allocate CO order step 4
        alloc_id = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value][JavaApiFields.ClientAllocID.value]
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)

        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.alloc_account,
            'AllocQty': self.qty,
            'AvgPx': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message(f'Allocate block ', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                                              JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
                                              JavaApiFields.WashBookAccountID.value: self.washbook},
                                             confirmation_report,
                                             'Check expected and actually result from step 4')
        # endregion
