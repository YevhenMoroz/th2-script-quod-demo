import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7012(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.submit_request2 = OrderSubmitOMS(self.data_set)
        self.cancel_request = CancelOrderRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        order_submit = self.submit_request.set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.java_api_manager.send_message_and_receive_response(order_submit)
        res = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        ord_id = res.get_parameter("OrdReplyBlock")["OrdID"]
        order_submit = self.submit_request2.set_default_child_dma(ord_id)
        route = self.data_set.get_route_id_by_name("route_1")
        order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                {"RouteList": {"RouteBlock": [{"RouteID": route}]}})

        self.ssh_client.send_command("qstop -id QUOD.ESBUYTH2TEST")
        time.sleep(3)
        self.java_api_manager.send_message_and_receive_response(order_submit)
        res = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values({"UnmatchedQty": "0.0"},
                                             res.get_parameter("OrdUpdateBlock"),
                                             "compare UnmatchedQty in the OrdUpdate")

        res = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        child_ord_id = res.get_parameter("OrdNotificationBlock")["OrdID"]
        self.cancel_request.set_default(child_ord_id)
        self.cancel_request.update_fields_in_component("OrderCancelRequestBlock", {'ForcedCancel': 'Y'})
        self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        res = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values({"UnmatchedQty": "100.0"},
                                             res.get_parameter("OrdUpdateBlock"),
                                             "compare UnmatchedQty in the OrdUpdate")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.send_command("qstart ESBUYTH2TEST")
