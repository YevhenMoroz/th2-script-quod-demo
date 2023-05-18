import logging
from pathlib import Path

from custom.basic_custom_actions import create_event
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    SubmitRequestConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9201(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.qty = "100"
        self.price = "10"
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.account = self.data_set.get_account_by_name("client_pt_1_acc_1")
        self.account2 = self.data_set.get_account_by_name("client_pt_1_acc_2")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        ord_id = order_reply.get_parameter("OrdReplyBlock")["OrdID"]
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        self.java_api_manager.send_message(self.trade_request)

        self.complete_order.set_default_complete(ord_id)
        self.java_api_manager.send_message(self.complete_order)

        self.allocation_instruction.set_default_book(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)

        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        alloc_id = alloc_report_message.get_parameter("AllocationReportBlock")["ClientAllocID"]
        # endregion

        # region Step 1 - Approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        # endregion

        # region Step 2 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.account,
                "AllocQty": self.qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)

        conf_report_message = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value
                                                                     ).get_parameters()["ConfirmationReportBlock"]
        conf_id = conf_report_message['ConfirmationID']
        self.java_api_manager.compare_values({'AllocAccountID': self.account}, conf_report_message,
                                             "Check account")
        # endregion

        # region amend allocation
        self.confirmation_request.set_default_amend_allocation(conf_id, alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                             {'AllocAccountID': self.account2})
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)

        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        self.java_api_manager.compare_values({'AllocAccountID': self.account2}, conf_report_message,"Check new account")

        # endregion
