import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7291(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty_dma = "40"
        self.price_dma = "10"
        self.fix_message_dma.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty_dma}, "Price": self.price_dma})
        self.fix_message_care = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty_care = "50"
        self.price_care = "20"
        self.fix_message_care.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty_care}, "Price": self.price_care})
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.suspend_request = SuspendOrderManagementRequest()
        self.match_request = ManualMatchExecToParentOrdersRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price_dma), float(self.price_dma),
                                                                         int(self.qty_dma), int(self.qty_dma), 1)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_dma)
            exec_id_dma = self.fix_manager.get_last_message("ExecutionReport").get_parameter("ExecID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region Step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {"OrdQty": self.qty_care, "Price": self.price_care})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id_care = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
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
        self.match_request.set_default(ord_id_care, self.qty_dma, exec_id_dma)
        self.java_api_manager.send_message_and_receive_response(self.match_request)
        match_reply = self.java_api_manager.get_last_message(
            CSMessageType.ManualMatchExecToParentOrdersReply.value).get_parameters()["MessageReply"][
            "MessageReplyBlock"][0]
        self.java_api_manager.compare_values({"ErrorCD": "QUOD-16533"}, match_reply, "Check that request not allowed")
        # endregion
