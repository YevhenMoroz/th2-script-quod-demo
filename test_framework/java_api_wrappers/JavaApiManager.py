import ast
import importlib
import logging
import re
from enum import Enum

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest, ActJavaSubmitMessageResponses

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod, Verifier
from stubs import Stubs
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType, ESMessageType, PKSMessageType, \
    MDAMessageType, AQSMessageType, QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


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

    def send_message_and_receive_response(self, message: JavaApiMessage, filter_dict=None, response_time=None):
        logging.info(f"Message {message.get_message_type()} sent with params -> {message.get_parameters()}")
        if message.get_message_type() == ORSMessageType.FixNewOrderSingle.value and filter_dict != ExtractAllMessages.All.value:
            response = self.act.submitFixNewOrderSingle(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.FixNewOrderSingle.value and filter_dict == ExtractAllMessages.All.value:
            response = self.act.submitFixNewOrderSingleWithExtractionAllMessages(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderSubmit.value:
            response = self.act.submitOrderSubmit(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.TradeEntryRequest.value:
            if "OrdID" in message.get_parameter("TradeEntryRequestBlock"):
                response = self.act.submitTradeEntry(
                    request=ActJavaSubmitMessageRequest(
                        message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                                 message.get_parameters(), self.get_session_alias()),
                        parent_event_id=self.get_case_id(), response_time=response_time))
            else:
                response = self.act.submitTradeEntryFX(
                    request=ActJavaSubmitMessageRequest(
                        message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                                 message.get_parameters(), self.get_session_alias()),
                        parent_event_id=self.get_case_id()))
        elif message.get_message_type() == ORSMessageType.OrderSubmit.value:
            response = self.act.submitOrderSubmit(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))

        elif message.get_message_type() == ORSMessageType.OrderCancelRequest.value:
            response = self.act.submitOrderCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.DFDManagementBatch.value and filter_dict is None:
            response = self.act.submitDFDManagementBatch(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.AllocationInstruction.value:
            response = self.act.submitAllocationInstruction(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.ForceAllocInstructionStatusRequest.value:
            response = self.act.submitForceAllocInstructionStatusRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.Confirmation.value:
            response = self.act.submitConfirmation(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == CSMessageType.CDOrdAckBatchRequest.value:
            response = self.act.submitCDOrdAckBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.BlockUnallocateRequest.value:
            response = self.act.submitOrderBlockUnallocateRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.BookingCancelRequest.value:
            response = self.act.submitOrderBookingCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.NewOrderList.value:
            response = self.act.submitNewOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderListWaveCreationRequest.value:
            response = self.act.submitOrderListWaveCreationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.ManualOrderCrossRequest.value:
            response = self.act.submitManualOrderCrossRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.UnMatchRequest.value:
            response = self.act.submitOrderUnMatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(), message.get_parameters(),
                                                             self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))

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
                    parent_event_id=self.get_case_id(), response_time=response_time))
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
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveRequest.value:
            response = self.act.submitOrderBagWaveRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveModificationRequest.value:
            response = self.act.submitOrderBagWaveModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderBagWaveCancelRequest.value:
            response = self.act.submitOrderBagWaveCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderBagDissociateRequest.value:
            response = self.act.submitOrderBagDissociateRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.QuoteRequest.value:
            response = self.act.submitFixQuoteRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.QuoteRequestActionRequest.value:
            response = self.act.submitQuoteRequestActionRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.PositionTransferInstruction.value:
            response = self.act.submitPositionTransferInstructionRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ESMessageType.ExecutionReport.value and filter_dict is None:
            response = self.act.submitExecutionReport(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))

        elif message.get_message_type() == ORSMessageType.ComputeBookingFeesCommissionsRequest.value:
            response = self.act.submitComputeBookingFeesCommissionsRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == PKSMessageType.FixRequestForPositions.value:
            response = self.act.submitFixRequestForPositions(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.DFDManagementBatch.value and filter_dict is not None:
            response = self.act.submitMassDFDManagementBatch(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.BlockChangeConfirmationServiceRequest.value:
            response = self.act.submitBlockChangeConfirmationServiceRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.CheckOutOrderRequest.value:
            response = self.act.submitCheckOutOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.ForceAllocInstructionStatusBatchRequest.value:
            response = self.act.submitForceAllocInstructionStatusBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.BlockUnallocateBatchRequest.value:
            response = self.act.submitBlockUnallocateBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ESMessageType.ExecutionReport.value:
            response = self.act.submitExecutionReportWithFilter(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ESMessageType.OrdReport.value:
            response = self.act.submitOrdReport(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.MassConfirmation.value:
            response = self.act.submitMassConfirmation(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == MDAMessageType.MarketDataRequest.value:
            response = self.act.submitMarketDataRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.NewOrderReply.value:
            response = self.act.submitNewOrderReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.CheckInOrderRequest.value:
            response = self.act.submitCheckInOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.HeldOrderAckRequest.value:
            response = self.act.submitHeldOrderAck(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.MarkOrderRequest.value:
            response = self.act.submitMarkOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ESMessageType.OrderCancelReply.value:
            response = self.act.submitOrderCancelReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ESMessageType.OrderModificationReply.value:
            response = self.act.submitOrderModificationReply(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.RemoveOrdersFromOrderListRequest.value:
            response = self.act.submitRemoveOrdersFromOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.ListCancelRequest.value:
            response = self.act.submitListCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.AddOrdersToOrderListRequest.value:
            response = self.act.submitAddOrdersToOrderListRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderListWaveModificationRequest.value:
            response = self.act.submitOrderListWaveModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderActionRequest.value:
            response = self.act.submitOrderActionRequestWithFilter(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.SuspendOrderManagementRequest.value:
            response = self.act.submitSuspendOrderManagementRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == CSMessageType.ManualMatchExecToParentOrdersRequest.value:
            response = self.act.submitManualMatchExecToParentOrdersRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.FixOrderModificationRequest.value:
            response = self.act.submitFixOrderModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.FixOrderCancelRequest.value:
            response = self.act.submitFixOrderCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == CSMessageType.CDTransferRequest.value:
            response = self.act.submitCDTransferRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == CSMessageType.CDTransferAck.value:
            response = self.act.submitCDTransferAckRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == CSMessageType.CDOrdAssign.value:
            response = self.act.submitCDOrdAssign(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), response_time=response_time))
        elif message.get_message_type() == ORSMessageType.TradeEntryBatchRequest.value:
            response = self.act.submitTradeEntryBatchRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == CSMessageType.ManualMatchExecsToParentOrderRequest.value:
            response = self.act.submitManualMatchExecsToParentOrderRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == AQSMessageType.FrontendQuery.value:
            response = self.act.submitFrontendQueryRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.OrderListWaveCancelRequest.value:
            response = self.act.submitOrderListWaveCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict))
        elif message.get_message_type() == ORSMessageType.NewOrderMultiLeg.value:
            response = self.act.submitNewOrderMultiLeg(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.FixAllocationInstruction.value:
            response = self.act.submitFixAllocationInstruction(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.PositionTransferCancelRequest.value:
            response = self.act.submitPositionTransferCancelRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id()))
        elif message.get_message_type() == PKSMessageType.RequestForPositions.value:
            response = self.act.submitRequestForPosition(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.FixNewOrderList.value:
            response = self.act.submitFixNewOrderList(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == QSMessageType.QuoteManagementRequest.value:
            response = self.act.submitQuoteManagementRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == QSMessageType.ListingQuotingModificationRequest.value:
            response = self.act.submitListingQuotingModificationRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == QSMessageType.StopQuotingRequest.value:
            response = self.act.submitStopQuotingRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.CptyBlockRejectRequest.value:
            response = self.act.submitCptyBlockRejectRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.BlockValidateRequest.value:
            response = self.act.submitBlockValidateRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        elif message.get_message_type() == ORSMessageType.MatchCptyMOBlocksRequest.value:
            response = self.act.submitMatchCptyMOBlocksRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
                    parent_event_id=self.get_case_id(), filterFields=filter_dict, response_time=response_time))
        else:
            response = None
        return self.parse_response(response)

    def parse_response(self, response: ActJavaSubmitMessageResponses) -> list:
        key_list = response.DESCRIPTOR.fields_by_name.keys()
        repeated_composite_container = {key: getattr(response, key) for key in key_list}  # remove unwanted keys
        response_messages_list = str(repeated_composite_container["response_message"])
        start_sep = "'fields': "
        end_sep = ",\n 'metadata'"
        fields_list = []
        for fields in response_messages_list.split(start_sep):
            if end_sep in fields:
                fields = re.sub('\"\n *\"', '', fields)  # in case of result on 2 lines
                fields_dict = ast.literal_eval(fields.split(end_sep)[0])  # get fields from message and parce it to dict
                fields_list.append(fields_dict)

        message_types = [
            message_type.metadata.message_type
            for message_type in response.response_message
        ]
        response_messages = []
        response_fix_message = None
        module_path = "test_framework.java_api_wrappers."
        for message_type, fields in zip(message_types, fields_list):
            for ors_message_type in ORSMessageType:
                if message_type == ors_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}ors_messages.{ors_message_type.name}"),
                                     ors_message_type.name)
                    response_fix_message = class_()
            for cs_message_type in CSMessageType:
                if message_type == cs_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}cs_message.{cs_message_type.name}"),
                                     cs_message_type.name)
                    response_fix_message = class_()
            for es_message_type in ESMessageType:
                if message_type == es_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}es_messages.{es_message_type.name}"),
                                     es_message_type.name)
                    response_fix_message = class_()
            for aqs_message_type in AQSMessageType:
                if message_type == aqs_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}aqs_messages.{aqs_message_type.name}"),
                                     aqs_message_type.name)
                    response_fix_message = class_()
            for pks_message_type in PKSMessageType:
                if message_type == pks_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}pks_messages.{pks_message_type.name}"),
                                     pks_message_type.name)
                    response_fix_message = class_()
            for qs_message_type in QSMessageType:
                if message_type == qs_message_type.value:
                    class_ = getattr(importlib.import_module(f"{module_path}qs_messages.{qs_message_type.name}"),
                                     qs_message_type.name)
                    response_fix_message = class_()
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
                self.verifier.compare_values(
                    f"Compare: {k}", v, actual_values[k], verification_method
                )
        except KeyError:
            raise ValueError('\033[91m' + f"Element: {k} not found" + '\033[0m')
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
                if filter_value and filter_value not in str(res.get_parameters()):
                    continue
                self.response.reverse()
                return res
        raise ValueError('\033[91m' + f"{message_type} not found" + '\033[0m')

    def get_first_message(self, message_type, filter_value=None) -> JavaApiMessage:
        for res in self.response:
            if res.get_message_type() == message_type:
                if filter_value and filter_value not in str(res.get_parameters()):
                    continue
                self.response.reverse()
                return res
        raise ValueError('\033[91m' + f"{message_type} not found" + '\033[0m')

    def get_last_message_by_multiple_filter(self, message_type, filter_values: list) -> JavaApiMessage:
        self.response.reverse()
        sequence_of_flag = []
        for res in self.response:
            if res.get_message_type() == message_type:
                sequence_of_flag.extend(
                    False
                    for filter_value in filter_values
                    if filter_value not in str(res.get_parameters())
                )
                if False in sequence_of_flag:
                    sequence_of_flag.clear()
                    continue
                self.response.reverse()
                return res
        raise ValueError('\033[91m' + f"{message_type} not found" + '\033[0m')


class ExtractAllMessages(Enum):
    All = 'All'
