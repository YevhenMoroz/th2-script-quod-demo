import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7508(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.qty_to_exec = "20"
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        self.new_client = self.data_set.get_client_by_name("client_2")
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.modify_request = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()["OrderID"]
        # endregion

        # region manual execution
        self.trade_entry_request.set_default_trade(order_id, self.price, self.qty_to_exec)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check order's values after execution
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value
        )
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
                JavaApiFields.UnmatchedQty.value: str(int(self.qty) - int(self.qty_to_exec)) + ".0",
            },
            exec_report_block,
            "Check Execution",
        )
        # endregion

        # region modify order
        self.modify_request.set_default(self.data_set, order_id)
        self.modify_request.update_fields_in_component(
            "OrderModificationRequestBlock",
            {"AccountGroupID": self.new_client, "WashBookAccountID": "CareWB", "PosValidity": "DEL"},
        )
        self.java_api_manager.send_message_and_receive_response(self.modify_request)
        # endregion

        # region check error after modification
        ord_modify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderModificationReply.value
        ).get_parameter(JavaApiFields.OrderModificationReplyBlock.value)["OrdModify"]
        self.java_api_manager.compare_values(
            {JavaApiFields.FreeNotes.value: "Cannot modify AccountGroupID"}, ord_modify_block, "Check Error"
        )
        # endregion
