import logging

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest, ActJavaSubmitMessageResponses
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod, Verifier
from stubs import Stubs
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType, ESMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.cs_message.CDOrdNotif import CDOrdNotif
from test_framework.java_api_wrappers.es_messages.NewOrderReply import NewOrderReply
from test_framework.java_api_wrappers.es_messages.OrdReport import OrdReport
from test_framework.java_api_wrappers.es_messages.OrderCancelReply import OrderCancelReply
from test_framework.java_api_wrappers.fx.FixPositionReportFX import FixPositionReportFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionReplyFX import QuoteRequestActionReplyFX
from test_framework.java_api_wrappers.fx.QuoteRequestNotifFX import QuoteRequestNotifFX
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListReply import AddOrdersToOrderListReply
from test_framework.java_api_wrappers.ors_messages.AllocationReport import AllocationReport
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateBatchReply import BlockUnallocateBatchReply
from test_framework.java_api_wrappers.ors_messages.BookingCancelReply import BookingCancelReply
from test_framework.java_api_wrappers.ors_messages.CDNotifDealer import CDNotifDealer
from test_framework.java_api_wrappers.ors_messages.CheckInOrderReply import CheckInOrderReply
from test_framework.java_api_wrappers.ors_messages.CheckOutOrderReply import CheckOutOrderReply
from test_framework.java_api_wrappers.ors_messages.ComputeBookingFeesCommissionsReply import \
    ComputeBookingFeesCommissionsReply
from test_framework.java_api_wrappers.ors_messages.ConfirmationReport import ConfirmationReport
from test_framework.java_api_wrappers.ors_messages.DFDManagementBatchReply import DFDManagementBatchReply
from test_framework.java_api_wrappers.ors_messages.ExecutionReport import ExecutionReport
from test_framework.java_api_wrappers.ors_messages.FixConfirmation import FixConfirmation
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusBatchReply import \
    ForceAllocInstructionStatusBatchReply
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusRequest import \
    ForceAllocInstructionStatusRequest
from test_framework.java_api_wrappers.ors_messages.HeldOrderAckReply import HeldOrderAckReply
from test_framework.java_api_wrappers.ors_messages.ListCancelReply import ListCancelReply
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossReply import ManualOrderCrossReply
from test_framework.java_api_wrappers.ors_messages.MarkOrderReply import MarkOrderReply
from test_framework.java_api_wrappers.ors_messages.NewOrderListReply import NewOrderListReply
from test_framework.java_api_wrappers.ors_messages.OrdListNotification import OrdListNotification
from test_framework.java_api_wrappers.ors_messages.OrdNotification import OrdNotification
from test_framework.java_api_wrappers.ors_messages.OrdReply import OrdReply
from test_framework.java_api_wrappers.ors_messages.OrdUpdate import OrdUpdate
from test_framework.java_api_wrappers.ors_messages.OrderActionReply import OrderActionReply
from test_framework.java_api_wrappers.ors_messages.OrderBagCancelReply import OrderBagCancelReply
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationReply import OrderBagCreationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateReply import OrderBagDissociateReply
from test_framework.java_api_wrappers.ors_messages.OrderBagModificationReply import OrderBagModificationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagNotification import OrderBagNotification
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveCancelReply import OrderBagWaveCancelReply
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationReply import OrderBagWaveModificationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveNotification import OrderBagWaveNotification
from test_framework.java_api_wrappers.ors_messages.OrderListWaveModificationReply import OrderListWaveModificationReply
from test_framework.java_api_wrappers.ors_messages.OrderListWaveNotification import OrderListWaveNotification
from test_framework.java_api_wrappers.ors_messages.OrderModificationReply import OrderModificationReply
from test_framework.java_api_wrappers.ors_messages.PositionReport import PositionReport
from test_framework.java_api_wrappers.ors_messages.PositionTransferReport import PositionTransferReport
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListReply import RemoveOrdersFromOrderListReply
from test_framework.java_api_wrappers.ors_messages.TradeEntryNotif import Order_TradeEntryNotif
from test_framework.java_api_wrappers.ors_messages.UnMatchReply import UnMatchReply


class JavaApiManager:
    def __init__(self, session_alias, case_id=None):
        self.act = Stubs.act_java_api
        self.__session_alias = session_alias
        self.__case_id = case_id
        self.verifier = Verifier(self.__case_id)
        self.response = None

    def send_message(self, message: JavaApiMessage) -> None:
        logging.info(f"Message {message.get_message_type()} sent with params -> {message.get_parameters()}")
        self.act.sendMessage(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                         message.get_parameters(), self.get_session_alias()),
                parent_event_id=self.get_case_id()))

    def send_message_and_receive_response(self, message: JavaApiMessage, filter_dict=None):
        logging.info(f"Message {message.get_message_type()} sent with params -> {message.get_parameters()}")
        if message.get_message_type() == ORSMessageType.FixNewOrderSingle.value:
            response = self.act.submitFixNewOrderSingle(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderSubmit.value:
            response = self.act.submitOrderSubmit(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.TradeEntryRequest.value:
            response = self.act.submitTradeEntry(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderCancelRequest.value:
            response = self.act.submitOrderCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.DFDManagementBatch.value and filter_dict is None:
            response = self.act.submitDFDManagementBatch(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.AllocationInstruction.value:
            response = self.act.submitAllocationInstruction(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.ForceAllocInstructionStatusRequest.value:
            response = self.act.submitForceAllocInstructionStatusRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.Confirmation.value:
            response = self.act.submitConfirmation(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == CSMessageType.CDOrdAckBatchRequest.value:
            response = self.act.submitCDOrdAckBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.BlockUnallocateRequest.value:
            response = self.act.submitOrderBlockUnallocateRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.BookingCancelRequest.value:
            response = self.act.submitOrderBookingCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.NewOrderList.value:
            response = self.act.submitNewOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderListWaveCreationRequest.value:
            response = self.act.submitOrderListWaveCreationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.ManualOrderCrossRequest.value:
            response = self.act.submitManualOrderCrossRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.UnMatchRequest.value:
            response = self.act.submitOrderUnMatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(), message.get_parameters(),
                                                             self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderModificationRequest.value:
            response = self.act.submitOrderModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagCreationRequest.value:
            response = self.act.submitOrderBagCreationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagModificationRequest.value:
            response = self.act.submitOrderBagModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagCancelRequest.value:
            response = self.act.submitOrderBagCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveRequest.value:
            response = self.act.submitOrderBagWaveRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveModificationRequest.value:
            response = self.act.submitOrderBagWaveModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveCancelRequest.value:
            response = self.act.submitOrderBagWaveCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderBagDissociateRequest.value:
            response = self.act.submitOrderBagDissociateRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.QuoteRequest.value:
            response = self.act.submitFixQuoteRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.QuoteRequestActionRequest.value:
            response = self.act.submitQuoteRequestActionRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.PositionTransferInstruction.value:
            response = self.act.submitPositionTransferInstructionRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ESMessageType.ExecutionReport.value and filter_dict is None:
            response = self.act.submitExecutionReport(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))

        elif message.get_message_type() == ORSMessageType.ComputeBookingFeesCommissionsRequest.value:
            response = self.act.submitComputeBookingFeesCommissionsRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == PKSMessageType.FixRequestForPositions.value:
            response = self.act.submitFixRequestForPositions(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.DFDManagementBatch.value and filter_dict is not None:
            response = self.act.submitMassDFDManagementBatch(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.BlockChangeConfirmationServiceRequest.value:
            response = self.act.submitBlockChangeConfirmationServiceRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.CheckOutOrderRequest.value:
            response = self.act.submitCheckOutOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.ForceAllocInstructionStatusBatchRequest.value:
            response = self.act.submitForceAllocInstructionStatusBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.BlockUnallocateBatchRequest.value:
            response = self.act.submitBlockUnallocateBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ESMessageType.ExecutionReport.value:
            response = self.act.submitExecutionReportWithFilter(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ESMessageType.OrdReport.value:
            response = self.act.submitOrdReport(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.MassConfirmation.value:
            response = self.act.submitMassConfirmation(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.NewOrderReply.value:
            response = self.act.submitNewOrderReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.CheckInOrderRequest.value:
            response = self.act.submitCheckInOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.HeldOrderAckRequest.value:
            response = self.act.submitHeldOrderAck(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.MarkOrderRequest.value:
            response = self.act.submitMarkOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ESMessageType.OrderCancelReply.value:
            response = self.act.submitOrderCancelReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ESMessageType.OrderModificationReply.value:
            response = self.act.submitOrderModificationReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.RemoveOrdersFromOrderListRequest.value:
            response = self.act.submitRemoveOrdersFromOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.ListCancelRequest.value:
            response = self.act.submitListCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.AddOrdersToOrderListRequest.value:
            response = self.act.submitAddOrdersToOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.OrderListWaveModificationRequest.value:
            response = self.act.submitOrderListWaveModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))

        elif message.get_message_type() == ORSMessageType.OrderActionRequest.value:
            response = self.act.submitOrderActionRequestWithFilter(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))

        else:
            response = None
        return self.parse_response(response)

    def parse_response(self, response: ActJavaSubmitMessageResponses) -> list:
        response_messages = list()
        for message in response.response_message:
            fields = dict()
            for main_field in message.fields:
                fields_content = dict()
                # Simple field
                if message.fields[main_field].simple_value != "":
                    fields.update({main_field: message.fields[main_field].simple_value})
                else:
                    for field in message.fields[main_field].message_value.fields:
                        # Field
                        if message.fields[main_field].message_value.fields[field].simple_value != "":
                            fields_content.update(
                                {field: message.fields[main_field].message_value.fields[field].simple_value})
                        else:
                            # Simple Repeating Group
                            repeating_group_list = list()
                            for repeating_group in message.fields[main_field].message_value.fields[
                                field].list_value.values:
                                repeating_group_list_field = dict()
                                for repeating_group_field in repeating_group.message_value.fields:
                                    repeating_group_list_field.update({repeating_group_field:
                                                                           repeating_group.message_value.fields[
                                                                               repeating_group_field].simple_value})
                                repeating_group_list.append(repeating_group_list_field)
                            fields.update({main_field: {field: repeating_group_list}})
                            fields_content.update({field: repeating_group_list})
                            # Component
                            component_fields = dict()
                            for component_field in message.fields[main_field].message_value.fields[
                                field].message_value.fields:
                                if message.fields[main_field].message_value.fields[field].message_value.fields[
                                    component_field].simple_value != "":
                                    component_fields.update({component_field:
                                                                 message.fields[main_field].message_value.fields[
                                                                     field].message_value.fields[
                                                                     component_field].simple_value})
                                    fields_content.update({field: component_fields})
                                else:
                                    # Repeating Group
                                    repeating_group_list = list()
                                    for repeating_group in \
                                            message.fields[main_field].message_value.fields[field].message_value.fields[
                                                component_field].list_value.values:
                                        repeating_group_list_field = dict()
                                        for repeating_group_field in repeating_group.message_value.fields:
                                            repeating_group_list_field.update({repeating_group_field:
                                                                                   repeating_group.message_value.fields[
                                                                                       repeating_group_field].simple_value})
                                        repeating_group_list.append(repeating_group_list_field)
                                    if not bool(repeating_group_list):
                                        # Inner component
                                        inner_component_fields = dict()
                                        for inner_component_field in message.fields[main_field].message_value.fields[
                                            field].message_value.fields[component_field].message_value.fields:
                                            if \
                                                    message.fields[main_field].message_value.fields[
                                                        field].message_value.fields[
                                                        component_field].message_value.fields[
                                                        inner_component_field].simple_value != "":
                                                inner_component_fields.update({inner_component_field:
                                                                             message.fields[
                                                                                 main_field].message_value.fields[
                                                                                 field].message_value.fields[
                                                                                 component_field].message_value.fields[
                                                                                 inner_component_field].simple_value})
                                                fields_content.update({field: {component_fields: {inner_component_fields}}})
                                            else:
                                                # Inner Repeating Group
                                                inner_repeating_group_list = list()
                                                for inner_repeating_group in \
                                                        message.fields[main_field].message_value.fields[
                                                            field].message_value.fields[
                                                            component_field].message_value.fields[inner_component_field].list_value.values:
                                                    inner_repeating_group_list_field = dict()
                                                    for inner_repeating_group_field in inner_repeating_group.message_value.fields:
                                                        inner_repeating_group_list_field.update({inner_repeating_group_field:
                                                                                               inner_repeating_group.message_value.fields[
                                                                                                   inner_repeating_group_field].simple_value})
                                                    inner_repeating_group_list.append(inner_repeating_group_list_field)
                                                fields_content.update({field: {component_field:{inner_component_field:inner_repeating_group_list}}})
                                    else:
                                        fields_content.update({field: {component_field: repeating_group_list}})
                    fields.update({main_field: fields_content})
            message_type = message.metadata.message_type
            response_fix_message = None
            if message_type == ORSMessageType.OrdReply.value:
                response_fix_message = OrdReply()
            elif message_type == ORSMessageType.OrdNotification.value:
                response_fix_message = OrdNotification()
            elif message_type == ORSMessageType.ExecutionReport.value:
                response_fix_message = ExecutionReport()
            elif message_type == ORSMessageType.OrdUpdate.value:
                response_fix_message = OrdUpdate()
            elif message_type == ORSMessageType.AllocationReport.value:
                response_fix_message = AllocationReport()
            elif message_type == ORSMessageType.CDNotifDealer.value:
                response_fix_message = CDNotifDealer()
            elif message_type == ORSMessageType.ForceAllocInstructionStatusRequest.value:
                response_fix_message = ForceAllocInstructionStatusRequest()
            elif message_type == ORSMessageType.ConfirmationReport.value:
                response_fix_message = ConfirmationReport()
            elif message_type == CSMessageType.CDOrdNotif.value:
                response_fix_message = CDOrdNotif()
            elif message_type == ORSMessageType.TradeEntryNotif.value:
                response_fix_message = Order_TradeEntryNotif()
            elif message_type == ORSMessageType.NewOrderListReply.value:
                response_fix_message = NewOrderListReply()
            elif message_type == ORSMessageType.OrdListNotification.value:
                response_fix_message = OrdListNotification()
            elif message_type == ORSMessageType.OrderListWaveNotification.value:
                response_fix_message = OrderListWaveNotification()
            elif message_type == ORSMessageType.PositionReport.value:
                response_fix_message = PositionReport()
            elif message_type == ESMessageType.NewOrderReply.value:
                response_fix_message = NewOrderReply()
            elif message_type == ESMessageType.OrderCancelReply.value:
                response_fix_message = OrderCancelReply()
            elif message_type == ESMessageType.ExecutionReport.value:
                response_fix_message = ExecutionReport()
            elif message_type == ESMessageType.OrdReport.value:
                response_fix_message = OrdReport()
            elif message_type == ORSMessageType.ManualOrderCrossReply.value:
                response_fix_message = ManualOrderCrossReply()
            elif message_type == ORSMessageType.OrderModificationReply.value:
                response_fix_message = OrderModificationReply()
            elif message_type == ORSMessageType.OrderBagCreationReply.value:
                response_fix_message = OrderBagCreationReply()
            elif message_type == ORSMessageType.OrderBagNotification.value:
                response_fix_message = OrderBagNotification()
            elif message_type == ORSMessageType.OrderBagModificationReply.value:
                response_fix_message = OrderBagModificationReply()
            elif message_type == ORSMessageType.OrderBagCancelReply.value:
                response_fix_message = OrderBagCancelReply()
            elif message_type == ORSMessageType.OrderBagWaveNotification.value:
                response_fix_message = OrderBagWaveNotification()
            elif message_type == ORSMessageType.OrderBagWaveModificationReply.value:
                response_fix_message = OrderBagWaveModificationReply()
            elif message_type == ORSMessageType.OrderBagWaveCancelReply.value:
                response_fix_message = OrderBagWaveCancelReply()
            elif message_type == ORSMessageType.PositionTransferReport.value:
                response_fix_message = PositionTransferReport()
            elif message_type == ORSMessageType.ComputeBookingFeesCommissionsReply.value:
                response_fix_message = ComputeBookingFeesCommissionsReply()
            elif message_type == ORSMessageType.QuoteRequestNotif.value:
                response_fix_message = QuoteRequestNotifFX()
            elif message_type == ORSMessageType.QuoteRequestActionReply.value:
                response_fix_message = QuoteRequestActionReplyFX()
            elif message_type == PKSMessageType.FixRequestForPositions.value:
                response_fix_message = FixPositionReportFX()
            elif message_type == ORSMessageType.BookingCancelReply.value:
                response_fix_message = BookingCancelReply()
            elif message_type == ORSMessageType.CheckOutOrderReply.value:
                response_fix_message = CheckOutOrderReply()
            elif message_type == ORSMessageType.ForceAllocInstructionStatusBatchReply.value:
                response_fix_message = ForceAllocInstructionStatusBatchReply()
            elif message_type == ORSMessageType.BlockUnallocateBatchReply.value:
                response_fix_message = BlockUnallocateBatchReply()
            elif message_type == ORSMessageType.OrderUnMatchReply.value:
                response_fix_message = UnMatchReply()
            elif message_type == ORSMessageType.FixConfirmation.value:
                response_fix_message = FixConfirmation()
            elif message_type == ORSMessageType.CheckInOrderReply.value:
                response_fix_message = CheckInOrderReply()
            elif message_type == ORSMessageType.HeldOrderAckReply.value:
                response_fix_message = HeldOrderAckReply()
            elif message_type == ORSMessageType.MarkOrderReply.value:
                response_fix_message = MarkOrderReply()
            elif message_type == ORSMessageType.RemoveOrdersFromOrderListReply.value:
                response_fix_message = RemoveOrdersFromOrderListReply()
            elif message_type == ORSMessageType.OrderBagDissociateReply.value:
                response_fix_message = OrderBagDissociateReply()
            elif message_type == ORSMessageType.DFDManagementBatchReply.value:
                response_fix_message = DFDManagementBatchReply()
            elif message_type == ORSMessageType.ListCancelReply.value:
                response_fix_message = ListCancelReply()
            elif message_type == ORSMessageType.AddOrdersToOrderListReply.value:
                response_fix_message = AddOrdersToOrderListReply()
            elif message_type == ORSMessageType.OrderListWaveModificationReply.value:
                response_fix_message = OrderListWaveModificationReply()
            elif message_type == ORSMessageType.OrderActionReply.value:
                response_fix_message = OrderActionReply()
            response_fix_message.change_parameters(fields)
            response_messages.append(response_fix_message)
        self.response = response_messages
        return response_messages

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def get_session_alias(self):
        return self.__session_alias

    def set_session_alias(self, session_alias):
        self.__session_alias = session_alias

    def compare_values(self, expected_values: dict, actual_values: dict, event_name: str,
                       verification_method: VerificationMethod = VerificationMethod.EQUALS):
        self.verifier.set_event_name(event_name)
        try:
            for k, v in expected_values.items():
                self.verifier.compare_values("Compare: " + k, v, actual_values[k],
                                             verification_method)
        except KeyError:
            raise KeyError(f"Element: {k} not found")
        self.verifier.verify()
        self.verifier = Verifier(self.__case_id)

    def key_is_absent(self, key: str, actual_values: dict, event_name: str):
        if key in actual_values:
            self.verifier.success = False

        self.verifier.fields.update(
            {"Is absent:": {"expected": key, "key": False, "type": "field",
                            "status": "PASSED" if self.verifier.success else "FAILED"}})
        self.verifier.set_event_name(event_name)
        self.verifier.verify()
        self.verifier = Verifier(self.__case_id)

    def get_last_message(self, message_type, filter_value=None) -> JavaApiMessage:
        self.response.reverse()
        for res in self.response:
            if res.get_message_type() == message_type:
                if filter_value and str(res.get_parameters()).find(filter_value) == -1:
                    continue
                self.response.reverse()
                return res
        raise KeyError(f"{message_type} not found")

    def get_first_message(self, message_type, filter_value=None) -> JavaApiMessage:
        for res in self.response:
            if res.get_message_type() == message_type:
                if filter_value and str(res.get_parameters()).find(filter_value) == -1:
                    continue
                self.response.reverse()
                return res
        raise KeyError(f"{message_type} not found")
