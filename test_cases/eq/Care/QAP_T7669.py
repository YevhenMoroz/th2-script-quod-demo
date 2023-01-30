import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, CDResponsesConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderModificationRequestOMS import \
    FixOrderModificationRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7669(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.order_cancel_replace_request = FixOrderModificationRequestOMS(self.data_set)
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.client = self.data_set.get_client_by_name('client_2')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.price = '4'
        self.qty = '444'
        self.qty_2 = '555'
        self.price_2 = '5'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1:  region create CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.new_order_single.set_default_care_limit()
        self.new_order_single.update_fields_in_component('NewOrderSingleBlock', {'Price': self.price,
                                                                                 'OrdQty': self.qty})
        self.new_order_single.update_fields_in_component('NewOrderSingleBlock', {'ClientAccountGroupID': self.client})
        self.java_api_manager2.send_message_and_receive_response(self.new_order_single)
        cd_ord_notif = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             cd_ord_notif[JavaApiFields.OrdNotificationBlock.value],
                                             'Verifying that CO orders has Sts = Sent (step 1)')
        # endregion

        # region step 2: accept CO order
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verifying that CO orders has Sts = Open (step 2)')
        # endregion

        # region step 3: Send OrderCancelReplaceRequest
        tuple_reply = self._send_order_modification_request(cl_ord_id, self.qty_2, self.price, 'step 3')
        cd_ord_notif_message = tuple_reply[0]
        qty_for_verification = tuple_reply[1]
        # endregion

        # region step 4: Accept request
        expected_result = {JavaApiFields.OrdQty.value: qty_for_verification}
        self._accept(cd_ord_notif_message, order_id, desk, expected_result, 'step 4')
        # endregion

        # region step 5: Send OrderCancelReplaceRequest
        tuple_reply = self._send_order_modification_request(cl_ord_id, self.qty_2, self.price_2, 'step 5')
        cd_ord_notif_message = tuple_reply[0]
        price_for_verification = tuple_reply[2]
        # endregion

        # region step 6: Accept reqeust
        expected_result = {JavaApiFields.Price.value: price_for_verification}
        self._accept(cd_ord_notif_message, order_id, desk, expected_result, 'step 6')
        # endregion

        # region step 7: Send OrderCancelRequest
        self.cancel_request.set_default_cancel(cl_ord_id)
        self.java_api_manager2.send_message_and_receive_response(self.cancel_request)
        cd_ord_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        self.java_api_manager2.compare_values(
            {JavaApiFields.CDRequestType.value: CDResponsesConst.CDRequestType_MOD.value},
            cd_ord_notif_message, f'Verifying {JavaApiFields.CDRequestType.value}  step 7')
        # endregion

        # region step 8: Accept request
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, 'C')
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value:OrderReplyConst.TransStatus_CXL.value}, order_reply,
                                             f'Verifying expected and actually result from step 8')
        # endregion

    def _send_order_modification_request(self, cl_ord_id, qty, price, step):
        self.order_cancel_replace_request.set_modify_order_limit(cl_ord_id, qty, price)
        self.java_api_manager2.send_message_and_receive_response(self.order_cancel_replace_request)
        cd_ord_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        qty_for_verification = str(float(qty))
        price = str(float(price))
        self.java_api_manager2.compare_values({JavaApiFields.OrdQty.value: qty_for_verification,
                                               JavaApiFields.Price.value: price},
                                              cd_ord_notif_message[
                                                  JavaApiFields.OrderModificationNotificationBlock.value],
                                              f'Verifying expected and actually result for {step}')
        self.java_api_manager2.compare_values({JavaApiFields.CDRequestType.value: CDResponsesConst.CDRequestType_MOD.value},
                                              cd_ord_notif_message, f'Verifying {JavaApiFields.CDRequestType.value} {step}')
        return cd_ord_notif_message, qty_for_verification, price

    def _accept(self, cd_ord_notif_message, order_id, desk, expected_result, step):
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, 'M')
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(expected_result, order_reply,
                                             f'Verifying expected and actually result from {step}')
