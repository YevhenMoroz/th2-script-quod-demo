import logging
from datetime import datetime, timedelta
from pathlib import Path
from pandas import Timestamp as tm
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7215(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.nos_request = FixNewOrderSingleOMS(self.data_set)
        self.modify_request = OrderModificationRequest()
        self.cancel_request = CancelOrderRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        nos_request = self.nos_request.set_default_care_limit()
        day = str(
            (tm(datetime.utcnow().isoformat()) + timedelta(days=3)).date().strftime('%Y-%m-%dT%H:%M:%S'))
        nos_request.update_fields_in_component("NewOrderSingleBlock", {"SettlDate": day})
        self.java_api_manager.send_message_and_receive_response(nos_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        self.java_api_manager.compare_values({"SettlDate": day[:-8]}, ord_notif.get_parameter("OrdNotificationBlock"),
                                             "Compare SettlDate", VerificationMethod.CONTAINS)
        # endregion
        # region Step 3-4
        nos_request.remove_fields_from_component("NewOrderSingleBlock", ["SettlDate"])
        day = str(
            (tm(datetime.utcnow().isoformat()) + timedelta(days=2)).date().strftime('%Y-%m-%dT%H:%M:%S'))
        self.java_api_manager.send_message_and_receive_response(nos_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        self.java_api_manager.compare_values({"SettlDate": day[:-8]}, ord_notif.get_parameter("OrdNotificationBlock"),
                                             "Compare SettlDate", VerificationMethod.CONTAINS)
        # endregion
        # region Step 5
        submit_request = self.submit_request.set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.java_api_manager.send_message_and_receive_response(submit_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        self.java_api_manager.compare_values({"SettlDate": day[:-8]}, ord_notif.get_parameter("OrdNotificationBlock"),
                                            "Compare SettlDate", VerificationMethod.CONTAINS)
        # endregion
        # region Step 6
        modify_request = self.modify_request.set_default(self.data_set,
                                                         ord_notif.get_parameter("OrdNotificationBlock")["OrdID"])
        day = str(
            (tm(datetime.utcnow().isoformat()) + timedelta(days=5)).date().strftime('%Y-%m-%dT%H:%M:%S'))
        modify_request.update_fields_in_component("OrderModificationRequestBlock", {"SettlDate": day})
        self.java_api_manager.send_message_and_receive_response(modify_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        self.java_api_manager.compare_values({"SettlDate": day[:-8]}, ord_notif.get_parameter("OrdReplyBlock"),
                                             "Compare SettlDate", VerificationMethod.CONTAINS)
        # endregion


