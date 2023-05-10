import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7657(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2")
        self.trd_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.nos.set_default_care_limit()
        qty = str(float(self.nos.get_parameters()["NewOrderSingleBlock"]["OrdQty"]))
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.client})
        self.java_api_manager2.send_message_and_receive_response(self.nos)
        order_id = self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.ClOrdID.value]
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        self.accept_request.set_default(order_id, cd_order_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        self.trd_request.set_default_trade(order_id, exec_qty="1")
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_rep = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, exec_rep,
            'Checking execution')
        # endregion
        # # region Step 1
        self.cancel_request.set_default_cancel(cl_ord_id)
        self.java_api_manager2.send_message_and_receive_response(self.cancel_request)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        # endregion
        # region Step 2
        self.accept_request.set_default(order_id, cd_order_notif_id, desk, "C", True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_rep, "Check cancel not accepted")
        # endregion
