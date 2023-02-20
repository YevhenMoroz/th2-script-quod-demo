import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7380(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.suspend_request = SuspendOrderManagementRequest()
        self.cross_request = ManualOrderCrossRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id_care = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]

        self.order_submit2.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {'Side': 'Sell'})
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_id_care2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region Step 2
        self.suspend_request.set_default(ord_id_care)
        self.java_api_manager.send_message_and_receive_response(self.suspend_request)
        suspend_reply = self.java_api_manager.get_last_message(
            ORSMessageType.SuspendOrderManagementReply.value).get_parameter(
            JavaApiFields.SuspendOrderManagementReplyBlock.value)
        self.java_api_manager.compare_values({"OrdID": ord_id_care, "SuspendedCare": "Y"}, suspend_reply,
                                             "Check suspend")
        # endregion
        # region Step 3
        self.cross_request.set_default(self.data_set, ord_id_care, ord_id_care2)
        self.java_api_manager.send_message_and_receive_response(self.cross_request)
        cross_reply = self.java_api_manager.get_last_message(ORSMessageType.ManualOrderCrossReply.value).get_parameters(
        )["MessageReply"]["MessageReplyBlock"][0]
        self.java_api_manager.compare_values({"ErrorCD": "QUOD-11503"}, cross_reply, "Check cross not allowed")
        # endregion
