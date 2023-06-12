import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields, BasketMessagesConst, OrdListNotificationConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8462(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.accept_request = CDOrdAckBatchRequest()
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.note = "test note"
        self.route_id = self.data_set.get_route_id_by_name("route_1")
        self.create_basket = NewOrderListOMS(self.data_set)
        self.add_order_to_list = AddOrdersToOrderListRequest()
        self.fix_verifier_ss = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_bo = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.basket_name = 'QAP_T8462'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create Basket
        self.create_basket.set_default_order_list()
        self.create_basket.update_fields_in_component('NewOrderListBlock', {'OrderListName': self.basket_name})
        self.java_api_manager.send_message_and_receive_response(self.create_basket)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket (Step 1)')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region Step 2 - Create CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.new_order_single.set_default_care_limit()
        self.java_api_manager2.send_message_and_receive_response(self.new_order_single)
        cd_ord_notif = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        ord_notif = self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        cl_ord_id = ord_notif[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrdListNotificationConst.OrdStatus_SUB.value},
                                             ord_notif,
                                             'Check order status after order creation (Step 2)')
        # endregion

        # region Step 3 - Add CO to the basket
        self.add_order_to_list.set_default(order_id, list_id)
        self.java_api_manager.send_message_and_receive_response(self.add_order_to_list)
        list_notify_ord_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)[JavaApiFields.OrdIDList.value][JavaApiFields.OrdIDBlock.value]
        self.java_api_manager.compare_values({}, list_notify_ord_block, 'Check that order is added to the list (Step 3)')
        # endregion

        # region Step 4 - Reject order
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, set_reject=True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.OrdStatus_REJ.value},
                                             order_reply,
                                             'Check order status after Rejection (Step 4)')
        # endregion

        # region Step 5 - Check fix sell gtw
        ignored_fields = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                          'SettlCurrency', 'SettlDate', 'NoParty', 'tag5120', 'ExecBroker', 'OrigClOrdID']
        self.exec_report.set_default_rejected(self.fix_message)
        self.exec_report.change_parameters({'ClOrdID': cl_ord_id, 'OrderListName': self.basket_name})
        self.fix_verifier_ss.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_fields)
        # endregion

        # region Step 6 - Check fix BO gtw
        self.fix_verifier_bo.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_fields)
        # endregion
