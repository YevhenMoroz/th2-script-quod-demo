import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7286(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        self.ord_sub_message2 = OrderSubmitOMS(self.data_set)
        self.suspend_request = SuspendOrderManagementRequest()
        self.ord_mod_request = OrderModificationRequest()
        self.trd_request = TradeEntryOMS(self.data_set)
        self.cancel_request = CancelOrderRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.ord_sub_message.set_default_care_limit(self.environment.get_list_fe_environment()[0].user_1,
                                                    self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                    SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)["OrdID"]
        # endregion
        # region Step 1
        self.suspend_request.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.suspend_request)
        suspend_reply = self.java_api_manager.get_last_message(
            ORSMessageType.SuspendOrderManagementReply.value).get_parameter(
            JavaApiFields.SuspendOrderManagementReplyBlock.value)
        self.java_api_manager.compare_values({"OrdID": order_id, "SuspendedCare": "Y"}, suspend_reply, "Check suspend")
        # endregion
        # region Step 2-3
        new_price = "50.0"
        self.ord_mod_request.set_default(self.data_set, order_id).update_fields_in_component(
            "OrderModificationRequestBlock", {"Price": new_price})
        self.java_api_manager.send_message_and_receive_response(self.ord_mod_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({"Price": new_price}, order_reply, 'Checking that order have new price')
        # endregion
        # region Step 4
        self.suspend_request.set_default(order_id, "N")
        self.java_api_manager.send_message_and_receive_response(self.suspend_request)
        suspend_reply = self.java_api_manager.get_last_message(
            ORSMessageType.SuspendOrderManagementReply.value).get_parameter(
            JavaApiFields.SuspendOrderManagementReplyBlock.value)
        self.java_api_manager.compare_values({"OrdID": order_id, "SuspendedCare": "N"}, suspend_reply, "Check release")
        # endregion
        # region Step 5
        self.trd_request.set_default_trade(order_id, new_price, "25")
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Checking execution')
        # endregion
        # region Step 6
        self.suspend_request.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.suspend_request)
        suspend_reply = self.java_api_manager.get_last_message(
            ORSMessageType.SuspendOrderManagementReply.value).get_parameter(
            JavaApiFields.SuspendOrderManagementReplyBlock.value)
        self.java_api_manager.compare_values({"OrdID": order_id, "SuspendedCare": "Y"}, suspend_reply, "Check suspend2")
        # endregion
        # region Step 7
        self.ord_sub_message2 = OrderSubmitOMS(self.data_set)
        self.ord_sub_message2.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                     self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     SubmitRequestConst.USER_ROLE_1.value, order_id)
        self.ord_sub_message2.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": "1"})
        self.java_api_manager.send_message_and_receive_response(self.ord_sub_message2)
        ord_not = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)
        exp_res = {"OrdStatus": "REJ", "FreeNotes": "The order is suspended"}
        self.java_api_manager.compare_values(exp_res, ord_not, "Check child", VerificationMethod.CONTAINS)
        # endregion
        # region Step 8
        self.cancel_request.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        res = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({"TransStatus": "CXL"}, res, "Check order cancel")
        # endregion
