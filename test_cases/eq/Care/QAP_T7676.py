import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.cs_message.CDOrdAssign import CDOrdAssign
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7676(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.client = self.data_set.get_client_by_name('client_2')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity_2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager_2 = JavaApiManager(self.java_api_connectivity_2, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.cd_ord_assign = CDOrdAssign()
        self.qty = "900"
        self.price = "40"
        self.order_type = "Limit"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-6: Create CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit.set_default_care_market(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=desk,
                                                  role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {JavaApiFields.OrdQty.value: self.qty})
        self.java_api_manager_2.send_message_and_receive_response(self.order_submit)
        ord_notification_message = \
            self.java_api_manager_2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters() \
                [JavaApiFields.OrderNotificationBlock.value]
        order_id = ord_notification_message[JavaApiFields.OrdID.value]
        self.java_api_manager_2.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                               ord_notification_message,
                                               'Verifying that order has Sts = "Sent" (step 6)')
        # endregion

        # region step 7: reassign order to desk
        self.cd_ord_assign.set_default(order_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.cd_ord_assign)
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             ord_update,
                                             'Verifying that order has Sts = "Sent" after reassign to desk (step 7)')
        cd_ord_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        # endregion

        # region step 8-10 : Reject CO order
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, set_reject=True)
        self.java_api_manager_2.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager_2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager_2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_REJ.value},
            order_reply, 'Verifying that order "Rejected" (step 10)')
        # endregion
