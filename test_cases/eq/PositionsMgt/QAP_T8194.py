import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.base_window import BaseWindow

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8194(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.wash_book = self.data_set.get_washbook_account_by_name("washbook_account_2")
        self.recipient = self.data_set.get_recipient_by_name("recipient_user_1")
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(recipient=self.recipient, desk="1")
        self.base_window = BaseWindow(self.test_id, session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO order
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        responses = self.ja_manager.send_message_and_receive_response(self.order_submit)
        for response in responses:
            if response.get_message_type() == ORSMessageType.OrdNotification.value:
                res = response
        act_wash_book = res.get_parameter("OrdNotificationBlock")["WashBookAccountID"]
        self.base_window.compare_values({"WashBookAccountID": self.wash_book}, {"WashBookAccountID": act_wash_book},
                                        "check WashBookAccountID")
        # endregion
