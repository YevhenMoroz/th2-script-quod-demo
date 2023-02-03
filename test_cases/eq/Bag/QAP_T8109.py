import logging
import os
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, \
    SubmitRequestConst, OrderBagConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8109(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.order_submit3 = OrderSubmitOMS(self.data_set)
        self.order_submit4 = OrderSubmitOMS(self.data_set)
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.cancel_order = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        self.order_submit2.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        # endregion
        # region Step 2
        child_nos = self.order_submit3.set_default_child_care(self.username,
                                                              self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                              SubmitRequestConst.USER_ROLE_1.value, ord_id)
        child_nos2 = self.order_submit4.set_default_child_care(self.username,
                                                               self.environment.get_list_fe_environment()[0].desk_ids[
                                                                   0],
                                                               SubmitRequestConst.USER_ROLE_1.value, ord_id2)
        self.java_api_manager.send_message_and_receive_response(child_nos)
        child_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        self.java_api_manager.send_message_and_receive_response(child_nos2)
        child_ord_id2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region Step 3
        self.cancel_order.set_default(child_ord_id)
        self.java_api_manager.send_message_and_receive_response(self.cancel_order)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value}
        self.java_api_manager.compare_values(expected_result, ord_notify, "Check TransStatus")
        self.cancel_order.set_default(child_ord_id2)
        self.java_api_manager.send_message_and_receive_response(self.cancel_order)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(expected_result, ord_notify, "Check TransStatus 2")
        # endregion
        # region Step 4
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        orders_id = [ord_id, ord_id2]
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]

        self.java_api_manager.compare_values({JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value
                                              }, order_bag_notification, "Check OrderBagStatus")
        # endregion
