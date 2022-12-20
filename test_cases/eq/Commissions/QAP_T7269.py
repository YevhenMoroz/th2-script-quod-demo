import logging
import time
from datetime import datetime
from pathlib import Path

from custom.basic_custom_actions import create_event
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    SubmitRequestConst,
    OrderReplyConst,
    ExecutionReportConst,
    JavaApiFields,
    CommissionAmountTypeConst,
    CommissionBasisConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7269(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "20"
        self.bas_amt = self.data_set.get_comm_profile_by_name("bas_amt")
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.commission = self.data_set.get_commission_by_name("commission2")  # commission2
        self.client_A = self.data_set.get_client_by_name("client_com_2")  # CLIENT_COMM_2
        self.client_B = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.order_modification_request = OrderModificationRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7269
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        # first commission, commission2
        self.rest_commission_sender.set_modify_client_commission_message(
            commission=self.commission, client=self.client_A, comm_profile=self.bas_amt
        )
        self.rest_commission_sender.send_post_request()
        time.sleep(3)

        # second commission, commission1
        self.rest_commission_sender.set_modify_client_commission_message(
            client=self.client_B, comm_profile=self.perc_amt
        )
        self.rest_commission_sender.send_post_request()
        time.sleep(3)
        # endregion

        # region Step 1 - Create CO order
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client_A,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "AccountGroupID": self.client_A},
            order_reply,
            "Comparing Status of Care order",
        )
        # endregion

        # region Step 2 - Change client of order
        self.order_modification_request.set_default(self.data_set, ord_id)
        self.order_modification_request.remove_fields_from_component("OrderModificationRequestBlock", ["SettlCurrency"])
        self.order_modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"AccountGroupID": self.client_B}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_modification_request)
        class_name.print_message("AMEND ORDER", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "AccountGroupID": self.client_B},
            order_reply,
            "Comparing Client of Care order",
        )
        # endregion

        # region Step 3 - Execution of Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        class_name.print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            "ExecutionReportBlock"
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            "Comparing Execution status (TransExecStatus)",
        )
        expected_commissions: dict = {
            JavaApiFields.CommissionRate.value: "5.0",
            JavaApiFields.CommissionAmount.value: "100.0",
            JavaApiFields.CommissionCurrency.value: "EUR",
            JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_PCT.value,
        }
        self.java_api_manager.compare_values(
            expected_commissions,
            exec_report["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Checking Client Commission after Execute",
        )
        # endregion

        # region Step 4 - Complete CO
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        class_name.print_message("COMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
            },
            order_reply,
            "Comparing PostTradeStatus after Complete",
        )
        # endregion

        # region Step 5 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client_B,
                "ClientCommissionList": {"ClientCommissionBlock": [expected_commissions]},
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)

        alloc_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        # alloc_id = alloc_report_message["ClientAllocID"]
        self.java_api_manager.compare_values(
            expected_commissions,
            alloc_report_message["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Book",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
