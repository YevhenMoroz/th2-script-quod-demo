import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.ors_messages.MarkOrderRequest import MarkOrderRequest
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8254(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mark_ord = MarkOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        self.mark_ord.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.mark_ord)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "Y"}, ord_notify, "Check Reviewed status")
        # endregion
        # region Step 2
        self.mark_ord.set_default(order_id, "N")
        self.java_api_manager.send_message_and_receive_response(self.mark_ord)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "N"}, ord_notify, "Check Reviewed status")
        # endregion
