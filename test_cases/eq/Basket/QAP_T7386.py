import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7386(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.remove_order_fom_list_request = RemoveOrdersFromOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created first basket')
        list_id = order_list_notification['OrderListID']
        ord_id_1 = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][0][
            'OrdID']
        # endregion

        # region trade order
        self.trade_request.set_default_trade(ord_id_1)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_report_block = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report_block,
            'Check order is filled')
        # endregion

        # region remove order from basket
        self.remove_order_fom_list_request.set_default(ord_id_1, list_id)
        self.java_api_manager.send_message_and_receive_response(self.remove_order_fom_list_request)
        remove_ords_from_list_reply = \
        self.java_api_manager.get_last_message(ORSMessageType.RemoveOrdersFromOrderListReply.value).get_parameters()[
            JavaApiFields.RemoveOrdersFromOrderListReplyBlock.value]
        self.java_api_manager.compare_values(
            {'FreeNotes': f'Runtime error (order {ord_id_1} requested to be removed is Filled)'},
            remove_ords_from_list_reply, 'Check error in RemoveOrdersFromOrderListReply')
        # endregion
