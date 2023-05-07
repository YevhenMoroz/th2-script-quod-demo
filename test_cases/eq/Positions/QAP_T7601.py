import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7601(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.recipient = self.data_set.get_recipient_by_name("recipient_user_3")
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.order_submit2 = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.trd_req = ExecutionReportOMS(data_set)
        self.dfd_manage_batch = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        ord_id = ord_rep["OrdID"]
        self.ja_manager.compare_values({"WashBookAccountID": self.washbook_acc}, ord_rep, "Check WashBookAccountID")
        # endregion
        # region Step 2
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit2)
        ord_id2 = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        self.trd_req.set_default_trade(ord_id2)
        self.ja_manager.send_message_and_receive_response(self.trd_req)
        cum_buy_qty = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,[JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]["CumBuyQty"]
        # endregion
        # region Step 3
        self.trd_req.set_default_trade(ord_id)
        self.ja_manager.send_message_and_receive_response(self.trd_req)
        posit = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value, [JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        exp_cum_buy_qty = str(float(cum_buy_qty) + 100)
        self.ja_manager.compare_values({"CumBuyQty": exp_cum_buy_qty}, posit, "Check CumBuyQty increased")
        # endregion
        # region Step 4
        self.dfd_manage_batch.set_default_complete(ord_id)
        self.ja_manager.send_message_and_receive_response(self.dfd_manage_batch)
        # endregion
        # region Step 5
        self.allocation_instruction.set_default_book(ord_id)
        self.ja_manager.send_message_and_receive_response(self.allocation_instruction)
        posit = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,[JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({"CumBuyQty": cum_buy_qty}, posit, "Check CumBuyQty decreased")
        # endregion
