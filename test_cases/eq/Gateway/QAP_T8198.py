import logging
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, OrdListNotificationConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8198(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_2")  # CLIENT2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.new_ord_list = NewOrderListFromExistingOrders()
        self.basket_name = 'Basket_QAP_T8198'
        self.fix_verifier_sell = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_back_office = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.cancel_reject = FixMessageOrderCancelRejectReportOMS()
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create Care orders
        ord_id1, cl_ord_id1, desk_id1 = self.__create_and_accept_order('first')
        ord_id2, cl_ord_id2, desk_id2 = self.__create_and_accept_order('second')
        # endregion

        # region Step 1 - Create Basket with existing orders
        self.new_ord_list.set_default([ord_id1, ord_id2], self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.new_ord_list)
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameter(
                JavaApiFields.NewOrderListReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status (step 1)')
        # endregion

        # region Step 2 - Send cancel request
        self.cancel_request.set_default_cancel(cl_ord_id1)
        self.java_api_manager2.send_message_and_receive_response(self.cancel_request)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        # endregion

        # region Step 3 - Reject cancel request
        self.accept_request.set_default(ord_id1, cd_order_notif_id, desk_id1, "C", True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id1).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 3 - Checking that Cancel Request is rejected (Step 3)",
        )
        # endregion

        # region Step 4 - check cancel reject on the Sell Side
        cancel_ignored_fields = ['CxlRejResponseTo', 'Account', 'TransactTime']
        change_parameters1 = {
            "Account": self.client,
            "OrdStatus": '0',
            "OrderID": ord_id1,
            "ClOrdID": cl_ord_id1,
            "OrigClOrdID": cl_ord_id1, 'OrderListName': self.basket_name
        }
        self.cancel_reject.change_parameters(change_parameters1)
        self.fix_verifier_sell.check_fix_message_fix_standard(self.cancel_reject,
                                                              key_parameters=['ClOrdID', 'OrdStatus'],
                                                              ignored_fields=cancel_ignored_fields)
        # endregion

        # region Step 5 - check cancel reject on the BO
        self.fix_verifier_back_office.check_fix_message_fix_standard(self.cancel_reject,
                                                                     key_parameters=['ClOrdID', 'OrdStatus'],
                                                              ignored_fields=cancel_ignored_fields)
        # endregion

        # region Step 6 - Send cancel request
        self.cancel_request.set_default_cancel(cl_ord_id1)
        self.java_api_manager2.send_message_and_receive_response(self.cancel_request)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        # endregion

        # region Step 7 - Accept cancel request
        self.accept_request.set_default(ord_id1, cd_order_notif_id, desk_id1, "C")
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id1).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value},
            order_reply,
            "Step 3 - Checking that order is cancelled (Step 7)",
        )
        # endregion

        # region Step 8 - check execution report on the Sell Side
        ignored_fields = ['ExecID', 'GatingRuleCondName', 'OrderQtyData',
                          'LastQty', 'GatingRuleName',
                          'TransactTime', 'Side', 'AvgPx', 'Parties',
                          'SettlCurrency', 'SettlDate', 'Currency',
                          'TimeInForce', 'HandlInst',
                          'CxlQty', 'LeavesQty', 'CumQty', 'LastPx', 'OrdType',
                          'OrderCapacity', 'QtyType', 'Price',
                          'Instrument', 'QuodTradeQualifier', 'BookID', 'NoParty', 'tag5120',
                          'ExecBroker']
        change_parameters2 = {
            "ExecType": "4",
            "OrdStatus": "4",
            "Account": self.client,
            "ClOrdID": cl_ord_id1,
            'OrigClOrdID': cl_ord_id1,
            "OrderID": ord_id1,
            'OrderListName': self.basket_name
        }
        self.exec_report.change_parameters(change_parameters2)
        self.fix_verifier_sell.check_fix_message_fix_standard(self.exec_report,
                                                              key_parameters=['ClOrdID', 'OrdStatus'],
                                                              ignored_fields=ignored_fields)
        # endregion

        # region Step 9 - check execution report on the BO
        self.fix_verifier_back_office.check_fix_message_fix_standard(self.exec_report,
                                                                     key_parameters=['ClOrdID', 'OrdStatus'],
                                                                     ignored_fields=ignored_fields)
        # endregion

    def __create_and_accept_order(self, num_of_order: str):
        # region Precondition - Create CO order
        self.nos.set_default_care_limit()
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.client,
                                                                    "ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager2.send_message_and_receive_response(self.nos)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager2.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_notif_message,
            f"Comparing Status of {num_of_order} Care order (precondition)",
        )
        # endregion

        # region Accept CO order in Client Inbox
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            f"Comparing Status of {num_of_order} Care order after Accept",
        )
        # endregion
        return ord_id, cl_ord_id, desk_id
