import logging
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationRequest import \
    OrderBagWaveModificationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7374(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.bag_request = OrderBagCreationRequest()
        self.wave_request = OrderBagWaveRequest()
        self.wave_modification_request = OrderBagWaveModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        submit_request = self.submit_request.set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.java_api_manager.send_message_and_receive_response(submit_request)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        submit_request2 = submit_request.update_fields_in_component("NewOrderSingleBlock",
                                                                    {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(submit_request2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        bag_name = basic_custom_actions.client_orderid(9)
        self.bag_request.set_default("Split", bag_name, [ord_id, ord_id2])
        self.java_api_manager.send_message_and_receive_response(self.bag_request)
        bag_reply = self.java_api_manager.get_last_message("Order_OrderBagCreationReply")
        bag_id = bag_reply.get_parameter("OrderBagCreationReplyBlock")["OrderBagID"]
        # endregion
        # region Step 1 2
        self.wave_request.set_default(bag_id, "200", "LMT", "DAY")
        params = {"AlgoParametersBlock": {"AlgoType": "TWP", "ScenarioID": "2", "AlgoPolicyID": "1000029"},
                  "Price": "5"}
        self.wave_request.update_fields_in_component("OrderBagWaveRequestBlock", params)
        self.java_api_manager.send_message_and_receive_response(self.wave_request)
        wave_notify = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value).get_parameters()[
                "OrderBagWaveNotificationBlock"]
        self.java_api_manager.compare_values(params["AlgoParametersBlock"], wave_notify["AlgoParametersBlock"],
                                             "compare Algo parameters")
        self.wave_modification_request.set_default(wave_notify["OrderBagWaveID"], "LMT", "DAY")

        params = {"AlgoParametersBlock": {"AlgoType": "TYP", "ScenarioID": "3", "AlgoPolicyID": "1000029"},
                  "Price": "5"}
        self.wave_modification_request.update_fields_in_component("OrderBagWaveModificationRequestBlock", params)
        self.java_api_manager.send_message_and_receive_response(self.wave_modification_request)
        self.java_api_manager.compare_values(params["AlgoParametersBlock"], wave_notify["AlgoParametersBlock"],
                                             "compare Algo parameters")
        # endregion
