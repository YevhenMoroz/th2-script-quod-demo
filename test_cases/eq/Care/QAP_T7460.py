import logging
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7460(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.manual_cross = ManualOrderCrossRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region Precondition
        order_1 = self.submit_request.set_default_care_limit(self.data_set.get_recipient_by_name("recipient_user_1"),
                                                             "1")
        response1 = self.java_api_manager.send_message_and_receive_response(order_1)

        ord_id_1 = self.get_response_value(response1, ORSMessageType.OrdReply.value, "OrdReplyBlock", "OrdID")
        order_2 = order_1.update_fields_in_component("NewOrderSingleBlock", {"Side": "Sell",
                                                                             "ClOrdID": basic_custom_actions.client_orderid(
                                                                                 9)})
        response2 = self.java_api_manager.send_message_and_receive_response(order_2)
        ord_id_2 = self.get_response_value(response2, ORSMessageType.OrdReply.value, "OrdReplyBlock", "OrdID")
        qty = order_1.get_parameter("NewOrderSingleBlock")["OrdQty"]
        price = order_1.get_parameter("NewOrderSingleBlock")["Price"]
        self.manual_cross.set_default(self.data_set, ord_id_1, ord_id_2, exec_qty=qty, exec_price=price)
        response3 = self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        man_cross_id = self.get_response_value(response3, ORSMessageType.ManualOrderCrossReply.value,
                                               "ManualOrderCrossReplyBlock", "ManualOrderCrossID")
        # endregion
        # region Step 1
        new_qty = str(int(order_1.get_parameter("NewOrderSingleBlock")["OrdQty"]) / 2)
        new_price = str(int(order_1.get_parameter("NewOrderSingleBlock")["Price"]) / 2)
        self.manual_cross.update_fields_in_component("ManualOrderCrossRequestBlock",
                                                     {"ExecQty": new_qty, "ExecPrice": new_price,
                                                      'ManualOrderCrossTransType': 'Replace',
                                                      "ManualOrderCrossID": man_cross_id})
        response4 = self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        for res in response4:
            if res.get_message_type() == ORSMessageType.ExecutionReport.value:
                self.java_api_manager.compare_values({"ExecQty": new_qty, "ExecPrice": new_price},
                                                     res.get_parameter("ExecutionReportBlock"),
                                                     "compare executions qty and price")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def get_response_value(self, response, message_type, block, field):
        for res in response:
            if res.get_message_type() == message_type:
                return res.get_parameter(block)[field]
