import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8978(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.account = 'Dummy_Client'
        self.new_order_message = FixNewOrderSingleOMS(self.data_set)
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Send 35=D message
        self.new_order_message.set_default_care_limit()
        cl_ord_id = self.new_order_message.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.ClOrdID.value]
        self.new_order_message.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.account})
        self.java_api_manager.send_message_and_receive_response(self.new_order_message)
        order_notification = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value},
                                             order_notification, 'Verify that order has Sts = Held (step 1)')
        # endregion

        # region step 2-3:Cancel order via FixOrderCancelRequest
        self.cancel_request.set_default_cancel(cl_ord_id)
        self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        order_notification = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_CXL.value},
                                             order_notification, 'Verify that order has Sts = Cancel (step 2)')
        order_notification = str(order_notification)
        actually_result = order_notification.find(JavaApiFields.SubCounterpartList.value)
        if actually_result > 0:
            actually_result = True
        self.java_api_manager.compare_values({'SubCounterPartIsPresent': True},
                                             {'SubCounterPartIsPresent': actually_result},
                                             'Check that order has subCounterpart (step 3)')
        # endregion
