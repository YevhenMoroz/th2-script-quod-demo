import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, \
    SubscriptionRequestTypes, PosReqTypes, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CrossAnnouncement import CrossAnnouncement
from test_framework.java_api_wrappers.ors_messages.HeldOrderAckRequest import HeldOrderAckRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T11379(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_iceberg_limit()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.cross_announcement = CrossAnnouncement(self.data_set)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.reject_request = HeldOrderAckRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Create 2 CO orders
        orders_ids = []

        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        client = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.AccountGroupID.value]
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        listing_list = self.data_set.get_listing_id_by_name('listing_2')
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_list}]},
            JavaApiFields.InstrID.value: instrument_id
        })
        orders_ids.append(self._create_co_orders())
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {
                                                         JavaApiFields.ClOrdID.value: bca.client_orderid(6),
                                                         JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value
                                                     })
        orders_ids.append(self._create_co_orders())
        # endregion

        # region step 1-2 : Perform Market Cross action
        self.cross_announcement.set_default(orders_ids[0], orders_ids[1])
        self.ja_manager.send_message_and_receive_response(self.cross_announcement, {orders_ids[0]: orders_ids[0],
                                                                                    orders_ids[1]: orders_ids[1]})
        order_notification_first = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value, orders_ids[0]).get_parameters()[JavaApiFields.OrdNotificationBlock.value]
        child_order_id_first = order_notification_first[JavaApiFields.OrdID.value]
        # endregion

        # region step 3: Reject CO order
        self.reject_request.set_default(child_order_id_first, client, ack_type='R')
        self.ja_manager.send_message_and_receive_response(self.reject_request)
        order_notif = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value, child_order_id_first).get_parameters()[JavaApiFields.OrdNotificationBlock.value]
        self.ja_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value},
                                       order_notif, "Verifying that order is rejected (step 3)")
        # endregion

    def _create_co_orders(self):
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        return order_reply[JavaApiFields.OrdID.value]


