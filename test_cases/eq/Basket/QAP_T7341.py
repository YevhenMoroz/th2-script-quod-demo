
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest
from test_framework.fix_wrappers.FixManager import FixManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7341(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.message_order = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.add_order_request = AddOrdersToOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create basket
        self.list_creation_request.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region create CO
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.message_order)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region add order to basket
        self.add_order_request.set_default(order_id, list_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.add_order_request)
        # endregion

        # region check fields
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')['OrdIDList']['OrdIDBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdID.value: order_id}, list_notify_block[2],
            'Check order in the basket')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response