import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BasketMessagesConst, JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7393(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.list_creation_request = NewOrderListOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        self.list_creation_request.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        # endregion

        # get orders and basket ids
        list_id = list_notify_block['OrderListID']
        ord_id1 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        ord_id2 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][1]['OrdID']

        # region complete order
        self.complete_request.set_default_complete_for_some_orders([ord_id1, ord_id2])
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        # endregion

        # region check complete basket
        self.return_result(responses, ORSMessageType.OrdReply.value)
        list_notify_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListID.value: list_id,
             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_DFD.value}, list_notify_block,
            'Check fields after completing')
        # endregion

        # region uncomplete basket
        self.complete_request.update_fields_in_component('DFDManagementBatchBlock', {'SetDoneForDay': 'N'})
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        # endregion

        # region check uncomplete basket
        self.return_result(responses, ORSMessageType.OrdReply.value)
        list_notify_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListID.value: list_id,
             JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_ACT.value}, list_notify_block,
            'Check fields after upcompleting')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
