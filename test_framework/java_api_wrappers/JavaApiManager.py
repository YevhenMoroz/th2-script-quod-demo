from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest, ActJavaSubmitMessageResponses
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod, Verifier
from stubs import Stubs
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType, ESMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.cs_message.CDOrdNotif import CDOrdNotif
from test_framework.java_api_wrappers.es_messages.NewOrderReply import NewOrderReply
from test_framework.java_api_wrappers.es_messages.OrdReport import OrdReport
from test_framework.java_api_wrappers.ors_messages.AllocationReport import AllocationReport
from test_framework.java_api_wrappers.ors_messages.CDNotifDealer import CDNotifDealer
from test_framework.java_api_wrappers.ors_messages.ConfirmationReport import ConfirmationReport
from test_framework.java_api_wrappers.ors_messages.ExecutionReport import ExecutionReport
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusRequest import \
    ForceAllocInstructionStatusRequest
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossReply import ManualOrderCrossReply
from test_framework.java_api_wrappers.ors_messages.NewOrderListReply import NewOrderListReply
from test_framework.java_api_wrappers.ors_messages.OrdListNotification import OrdListNotification
from test_framework.java_api_wrappers.ors_messages.OrdNotification import OrdNotification
from test_framework.java_api_wrappers.ors_messages.OrdReply import OrdReply
from test_framework.java_api_wrappers.ors_messages.OrdUpdate import OrdUpdate
from test_framework.java_api_wrappers.ors_messages.OrderBagCancelReply import OrderBagCancelReply
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationReply import OrderBagCreationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagModificationReply import OrderBagModificationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagNotification import OrderBagNotification
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveCancelReply import OrderBagWaveCancelReply
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationReply import OrderBagWaveModificationReply
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveNotification import OrderBagWaveNotification
from test_framework.java_api_wrappers.ors_messages.TradeEntryNotif import Order_TradeEntryNotif


class JavaApiManager:
    def __init__(self, session_alias, case_id=None):
        self.act = Stubs.act_java_api
        self.__session_alias = session_alias
        self.__case_id = case_id
        self.verifier = Verifier(self.__case_id)
        self.response = None

    def send_message(self, message: JavaApiMessage) -> None:
        self.act.sendMessage(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                         message.get_parameters(), self.get_session_alias()),
                parent_event_id=self.get_case_id()))

    def send_message_and_receive_response(self, message: JavaApiMessage):
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
        elif message.get_message_type() == ORSMessageType.DFDManagementBatch.value:
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
        elif message.get_message_type() == ORSMessageType.ManualOrderCrossRequest.value:
            response = self.act.submitManualOrderCrossRequest(
                request=ActJavaSubmitMessageRequest(
                    message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                             message.get_parameters(), self.get_session_alias()),
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
        else:
            response = None
        return self.parse_response(response)

    def parse_response(self, response: ActJavaSubmitMessageResponses) -> list:
        response_messages = list()
        for message in response.response_message:
            fields = dict()
            for field in message.fields:
                # Field
                if message.fields[field].simple_value != "":
                    fields.update({field: message.fields[field].simple_value})
                else:
                    component_fields = dict()
                    # Component
                    for component_field in message.fields[field].message_value.fields:
                        if message.fields[field].message_value.fields[component_field].simple_value != "":
                            component_fields.update({component_field: message.fields[field].message_value.fields[
                                component_field].simple_value})
                            fields.update({field: component_fields})
                        else:
                            # Repeating Group
                            repeating_group_list = list()
                            for repeating_group in message.fields[field].message_value.fields[
                                component_field].list_value.values:
                                repeating_group_list_field = dict()
                                for repeating_group_field in repeating_group.message_value.fields:
                                    repeating_group_list_field.update({repeating_group_field:
                                                                           repeating_group.message_value.fields[
                                                                               repeating_group_field].simple_value})
                                repeating_group_list.append(repeating_group_list_field)
                            fields.update({field: {component_field: repeating_group_list}})
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
            elif message_type == ORSMessageType.PositionReport.value:
                response_fix_message = OrdListNotification()
            elif message_type == ESMessageType.NewOrderReply.value:
                response_fix_message = NewOrderReply()
            elif message_type == ESMessageType.ExecutionReport.value:
                response_fix_message = ExecutionReport()
            elif message_type == ESMessageType.OrdReport.value:
                response_fix_message = OrdReport()
            elif message_type == ORSMessageType.ManualOrderCrossReply.value:
                response_fix_message = ManualOrderCrossReply()
            elif message_type == ORSMessageType.OrderModificationReply.value:
                response_fix_message = ManualOrderCrossReply()
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
            print("Element: " + k + " not found")
        self.verifier.verify()
        self.verifier = Verifier(self.__case_id)

    def get_last_message(self, message_type) -> JavaApiMessage:
        self.response.reverse()
        for res in self.response:
            if res.get_message_type() == message_type:
                return res
        raise IOError(f"{message_type} not found")
