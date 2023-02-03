import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.cs_message.CDTransferAck import CDTransferAck
from test_framework.java_api_wrappers.cs_message.CDTransferRequest import CDTransferRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7248(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.transfer_request = CDTransferRequest()
        self.transfer_ack_request = CDTransferAck()
        self.trade_entry_oms = TradeEntryOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2")
        self.accept_request = CDOrdAckBatchRequest()
        self.qty = '200'
        self.price = '10'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        user_2 = self.environment.get_list_fe_environment()[0].user_1
        role = SubmitRequestConst.USER_ROLE_1.value
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit.set_default_care_limit(recipient=user_2,
                                                 desk=desk,
                                                 role=role)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {JavaApiFields.OrdQty.value: self.qty,
                                                                             JavaApiFields.Price.value: self.price})
        self.java_api_manager2.send_message_and_receive_response(self.order_submit)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        order_id = self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        self.accept_request.set_default(order_id, cd_order_notif_id, desk, set_reject=False)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Checking expected and actually result for (step 1)')
        # endregion

        # region step 2: Transfer order on user 2
        self.transfer_request.set_default_send_on_user(order_id, user_2, role, desk)
        self.java_api_manager2.send_message_and_receive_response(self.transfer_request)
        cd_transfer_reply = \
            self.java_api_manager2.get_last_message(CSMessageType.CDTransferReply.value).get_parameters()[
                JavaApiFields.CDTransferReplyBlock.value]
        cd_transfer_id = cd_transfer_reply[JavaApiFields.CDTransferID.value]
        # endregion

        # region step 3: Accept transfer order
        self.transfer_ack_request.set_default(cd_transfer_id, acceptor_desk_id=desk)
        self.java_api_manager.send_message_and_receive_response(self.transfer_ack_request,
                                                                filter_dict={order_id: order_id})
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.RecipientUserID.value: user_2},
                                             ord_update, 'Checking that "Recipient is user 2')

        # endregion

        # region step 4: Manual Execute CO order
        self.trade_entry_oms.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager2.send_message_and_receive_response(self.trade_entry_oms)
        execution_report = \
        self.java_api_manager2.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Checking that CO order executed (step 4)')
        # endregion
