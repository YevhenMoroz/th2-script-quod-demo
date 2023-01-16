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
    SubmitRequestConst, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8145(TestCase):
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
        self.order_submit5 = OrderSubmitOMS(self.data_set)
        self.order_submit6 = OrderSubmitOMS(self.data_set)
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.bag_modify = ModifyBagOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.order_submit.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        self.order_submit2.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
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
        orders_id = [child_ord_id, child_ord_id2]
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        self.java_api_manager.compare_values({'OrdID': child_ord_id},
                                             order_bag_notification["OrderBagOrderList"]["OrderBagOrderBlock"][0],
                                             "Check child order in bag")
        self.java_api_manager.compare_values({'OrdID': child_ord_id2},
                                             order_bag_notification["OrderBagOrderList"]["OrderBagOrderBlock"][1],
                                             "Check child order2 in bag")
        self.java_api_manager.compare_values({JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value
                                              }, order_bag_notification, "Check OrderBagStatus")
        # endregion
        # region Step 1
        self.order_submit5.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit5)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id3 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        # endregion
        # region Step 2
        child_nos3 = self.order_submit3.set_default_child_care(self.username,
                                                               self.environment.get_list_fe_environment()[0].desk_ids[0]
                                                               , SubmitRequestConst.USER_ROLE_1.value, ord_id3)
        self.java_api_manager.send_message_and_receive_response(child_nos3)
        child_ord_id3 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region Step 3
        self.bag_modify.set_default(bag_order_id, "20", bag_name)
        self.bag_modify.add_components_into_repeating_group('OrderBagOrderList', 'OrderBagOrderBlock', 'OrdID',
                                                            [child_ord_id, child_ord_id2, child_ord_id3])
        self.java_api_manager.send_message_and_receive_response(self.bag_modify)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values({'OrdID': child_ord_id3},
                                             order_bag_notification["OrderBagOrderList"]["OrderBagOrderBlock"][2],
                                             "Check child order3 in bag")
        self.java_api_manager.compare_values({JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value
                                              }, order_bag_notification, "Check OrderBagStatus after modification")
        # endregion
