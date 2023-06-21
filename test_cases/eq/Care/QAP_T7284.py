import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    ExecutionReportConst, AllocationReportConst, ConfirmationReportConst, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7284(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.mo_client = self.data_set.get_client_by_name('client_pt_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.security_account = self.data_set.get_account_by_name('client_pos_3_acc_3')  # PROP
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.unallocate_block = BlockUnallocateRequest()
        self.cancel_booking = BookingCancelRequest()
        self.request_for_position = RequestForPositions()
        self.unmatch_request = UnMatchRequest()
        self.qty = '1000'
        self.price = '2'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        listing = self.data_set.get_listing_id_by_name("listing_3")
        instrument = self.data_set.get_instrument_id_by_name("instrument_2")
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                       {JavaApiFields.ListingList.value: {
                                                           JavaApiFields.ListingBlock.value: [
                                                               {JavaApiFields.ListingID.value: listing}]},
                                                           JavaApiFields.InstrID.value: instrument,
                                                           JavaApiFields.OrdQty.value: self.qty,
                                                           JavaApiFields.AccountGroupID.value: self.mo_client,
                                                           JavaApiFields.Price.value: self.price})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply,
                                             'Verifying expected and actually result (step 1)')
        # endregion

        # region step 2: Fully Split CO order
        nos_rule = child_ord_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names, self.venue,
                int(self.price))
            self.submit_request.set_default_child_dma(order_id)
            self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                           {JavaApiFields.Price.value: self.price,
                                                            JavaApiFields.InstrID.value: instrument,
                                                            JavaApiFields.OrdQty.value: self.qty,
                                                            JavaApiFields.AccountGroupID.value: self.mo_client,
                                                            JavaApiFields.ExecutionPolicy.value: 'DMA'})
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                'Verifying expected and actually results (step 2)')
            child_ord_id = order_reply[JavaApiFields.OrdID.value]
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endergion

        # region step 3: Trade DMA order
        self.execution_report.set_default_trade(child_ord_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.LastTradedQty.value: self.qty,
            JavaApiFields.LastPx.value: self.price,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.LeavesQty.value: "0.0",
            JavaApiFields.CumQty.value: self.qty,
            JavaApiFields.AvgPrice.value: self.price
        })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id,
                                                                                        child_ord_id: child_ord_id})
        parent_execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        parent_exec_id = parent_execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.UnmatchedQty.value: '0.0'},
            parent_execution_report,
            f'Verifying expected and actually results for {order_id} (step 3)')
        child_execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                        child_ord_id).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value,
                                              JavaApiFields.ReportedCumQty.value: str(float(self.qty))},
                                             child_execution_report,
                                             f'Verifying expected and actually results for {child_ord_id} (step 3)')
        # endregion

        # region step 4 : Complete CO order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_dfd_and_pt = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                               JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}
        self.java_api_manager.compare_values(expected_dfd_and_pt, order_reply_message,
                                             'Verifying expected and actually results (step 4)')
        # endregion

        # region step 5 : Book CO order
        # part 1: Send Allocation Instruction:
        self.allocation_instruction_message.set_default_book(order_id)
        self.allocation_instruction_message.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                                       {JavaApiFields.AvgPx.value: self.price,
                                                                        JavaApiFields.InstrID.value: instrument,
                                                                        JavaApiFields.Qty.value: self.qty})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        # end_of_part

        # part 2: Verifying order level:
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        expected_dfd_and_pt.update({JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value})
        self.java_api_manager.compare_values(
            expected_dfd_and_pt,
            ord_update, f'Verifing that order {order_id} has PostTrade status = BKD (step 5)')
        # end_of_part

        # part 3 : Verifying block level
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        expected_result_block = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value})
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        alloc_id_booking = allocation_report[JavaApiFields.BookingAllocInstructionID.value]
        self.java_api_manager.compare_values(expected_result_block, allocation_report,
                                             f'Verifying that block {alloc_id} has properly statuses (step 5)')
        # end_of_part

        # endregion

        # region step 6 approve and allocate block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.approve_message)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value,
                                                             {
                                                                 JavaApiFields.InstrID.value: instrument,
                                                                 JavaApiFields.AllocQty.value: self.qty,
                                                                 JavaApiFields.AvgPx.value: self.price
                                                             })
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result_block.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                      JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                                      JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value})
        self.java_api_manager.compare_values(expected_result_block, allocation_report,
                                             f'Verify that block {alloc_id} has properly values (step 6)')
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_conf = {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        self.java_api_manager.compare_values(expected_result_conf,
                                             confirmation_report,
                                             'Verify that allocation created and has properly defined statuses (step 6)')

        # endregion

        # region step 7: Unallocate block
        self.unallocate_block.set_default(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.unallocate_block)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_conf.clear()
        expected_result_conf.update(
            {JavaApiFields.ConfirmTransType.value: ConfirmationReportConst.ConfirmTransType_CAN.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_CXL.value})
        self.java_api_manager.compare_values(
            expected_result_conf, confirmation_report, 'Verify that allocation is canceled (step 7)')
        # endregion

        # region step 8: UnBook order
        self.cancel_booking.set_default(alloc_id_booking)
        self.java_api_manager.send_message_and_receive_response(self.cancel_booking)
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        expected_dfd_and_pt.update({JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                                    JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value})
        self.java_api_manager.compare_values(expected_dfd_and_pt, ord_update,
                                             'Verify that order has properly values (step 8)')

        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result_block.clear()
        expected_result_block.update({JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
                                      JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_CXL.value})
        self.java_api_manager.compare_values(expected_result_block, allocation_report,
                                             'Verify that block is canceled (step 8)')
        # endregion

        # region step 9: Uncomplete CO order
        self.complete_request.set_default_uncomplete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        key_is_absent = not (JavaApiFields.DoneForDay.value in order_reply)
        self.java_api_manager.compare_values({'KeyIsAbsent': True}, {'KeyIsAbsent': key_is_absent},
                                             f'Verify that {JavaApiFields.DoneForDay.value} is empty (step 9)')
        key_is_absent = not (JavaApiFields.PostTradeStatus.value in order_reply)
        self.java_api_manager.compare_values({'KeyIsAbsent': True}, {'KeyIsAbsent': key_is_absent},
                                             f'Verify that {JavaApiFields.PostTradeStatus.value} is empty (step 9)')
        # endregion

        # region step 10: Perform unmatch and transfer
        pos_record = self._extract_position(self.security_account, instrument)
        posit_qty_before = pos_record[JavaApiFields.PositQty.value]
        self.unmatch_request.set_default(self.data_set, parent_exec_id, self.qty)
        self.unmatch_request.set_default_unmatch_and_transfer(self.security_account)
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   parent_exec_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
                                              JavaApiFields.UnmatchedQty.value: str(float(self.qty))},
                                             execution_report, 'Verify that expected result is achieved (step 10)')
        position_report = self._extract_position(self.security_account, instrument)
        self.java_api_manager.compare_values(
            {JavaApiFields.PositQty.value: str(float(posit_qty_before) + float(self.qty))},
            position_report, f'Verify that posit Qty of {self.security_account} increased on {self.qty} (step 10)')
        # endregion

    def _extract_position(self, account, instrument_id):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              account)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.java_api_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if instrument_id == position_record[JavaApiFields.InstrID.value] and position_record[
                JavaApiFields.PositionType.value] == 'N':
                return position_record
