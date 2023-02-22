import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7288(TestCase):
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
        new_qty = "400.0"
        self.ord_mod_request.set_default(self.data_set, order_id).update_fields_in_component(
            "OrderModificationRequestBlock", {"Price": new_price, "OrdQty": new_qty})
        self.java_api_manager.send_message_and_receive_response(self.ord_mod_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({"Price": new_price, "OrdQty": new_qty}, order_reply,
                                             'Checking that order have new price and qty')
        # endregion
