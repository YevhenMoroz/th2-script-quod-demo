import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, BagMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7338(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.bag_request = OrderBagCreationRequest()
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.bag_name = 'QAP_T7338'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        self.list_creation_request.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        self.return_result(responses, ORSMessageType.OrdListNotification.value)
        list_notify_block = self.result.get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        # endregion

        # region get orders id
        ord_id1 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        # endregion

        # region verifying of created bag
        self.bag_request.set_default('Split', self.bag_name, [ord_id1])
        responses = self.java_api_manager.send_message_and_receive_response(self.bag_request)
        self.return_result(responses, ORSMessageType.OrderBagNotification.value)
        bag_notify_block = self.result.get_parameter('OrderBagNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: BagMessagesConst.OrderBagStatus_NEW.value,
             'OrderBagOrderList': {'OrderBagOrderBlock': [{'OrdID': ord_id1}]}}, bag_notify_block,
            'Check created bag')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
