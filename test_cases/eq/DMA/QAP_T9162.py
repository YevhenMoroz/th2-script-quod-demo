import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9162(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.new_qty = "200"
        self.new_price = "30"
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.ord_rep = OrdReportOMS(self.data_set)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create order
        self.nos.update_fields_in_component("NewOrderReplyBlock",
                                            {"VenueAccount": {"VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)
        venue_ord_id = self.nos.get_parameter("NewOrderReplyBlock")["LastVenueOrdID"]
        qty = self.nos.get_parameter("NewOrderReplyBlock")["OrdQty"]
        price = self.nos.get_parameter("NewOrderReplyBlock")["Price"]
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep["OrdID"]
        expected_result = {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y",
                           "OrdQty": qty, "Price": price}
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check order status')
        # endregion
        # region
        self.ord_rep.set_default_open(order_id, venue_ord_id)
        self.ord_rep.update_fields_in_component("OrdReportBlock", {"Price": self.new_price, "VenueAccount":
            {"VenueActGrpName": self.venue_client_names}, "OrdQty": self.new_qty, "LeavesQty": self.new_qty,
                                                                   "ExecType": "Restated", "UnsolicitedOrder": "Yes"})

        self.java_api_manager.send_message_and_receive_response(self.ord_rep)
        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y",
                           "OrdQty": self.new_qty, "Price": self.new_price}
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check order status')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
