import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.es_messages.OrderCancelReply import OrderCancelReply
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.ors_messages.MarkOrderRequest import MarkOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8785(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.mark_ord = MarkOrderRequest()
        self.cancel_rep = OrderCancelReply()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.nos.update_fields_in_component("NewOrderReplyBlock",
                                            {"VenueAccount": {"VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep["OrdID"]
        ord_venue_id = self.nos.get_parameter("NewOrderReplyBlock")["LastVenueOrdID"]
        expected_result = {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y"}
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check order status')
        # endregion
        # region Step 2
        self.mark_ord.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.mark_ord)
        ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({"Reviewed": "Y"}, ord_notify, "Check Reviewed status")
        # endregion
        # region Step 3
        self.cancel_rep.set_default(self.data_set, order_id, ord_venue_id)
        self.cancel_rep.update_fields_in_component("OrderCancelReplyBlock", {"VenueAccount": {
            "VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.cancel_rep)
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: "ELI", "Reviewed": "N"}
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check order status')
        # endregion

