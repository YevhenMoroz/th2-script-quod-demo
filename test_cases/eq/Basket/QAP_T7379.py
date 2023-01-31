import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, \
    OrdListNotificationConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7379(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.wave_creation_request = OrderListWaveCreationRequest()

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

        # region get order_id
        list_id = list_notify_block['OrderListID']
        ord_id1 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        ord_id2 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][1]['OrdID']
        # endregion

        # region Wave
        self.wave_creation_request.set_default(list_id, ord_id_list=[ord_id1, ord_id2])
        responses = self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        self.return_result(responses, ORSMessageType.OrderListWaveNotification.value)
        list_wave_notify_block = self.result.get_parameter('OrderListWaveNotificationBlock')
        # endregion

        # region Verify wave
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_NEW.value},
            list_wave_notify_block,
            'Check created wave')
        # endregion

        # region Wave
        self.wave_creation_request.set_default(list_id, ord_id_list=[ord_id1, ord_id2])
        responses = self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        self.return_result(responses, ORSMessageType.OrderListWaveNotification.value)
        list_wave_notify_block = self.result.get_parameter('OrderListWaveNotificationBlock')
        # endregion

        # region check Error
        self.java_api_manager.compare_values(
            {JavaApiFields.FreeNotes.value: 'Empty wave'},
            list_wave_notify_block,
            'Check FreeNotes of wave')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
