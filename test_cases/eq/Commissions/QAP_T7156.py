import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    JavaApiFields,
    OrderReplyConst,
    ExecutionReportConst,
    CommissionAmountTypeConst,
    CommissionBasisConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7156(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "20"
        self.price = "20"
        self.qty_to_alloc = str(int(self.qty) // 2)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.client_acc_1 = self.data_set.get_account_by_name("client_com_1_acc_1")  # CLIENT_COMM_1_SA1
        self.client_acc_2 = self.data_set.get_account_by_name("client_com_1_acc_2")  # CLIENT_COMM_1_SA2
        self.comm1 = self.data_set.get_commission_by_name("commission1")
        self.comm2 = self.data_set.get_commission_by_name("commission2")
        self.comm_profile1 = self.data_set.get_comm_profile_by_name("perc_amt")
        self.comm_profile2 = self.data_set.get_comm_profile_by_name("perc_qty")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7156
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(
            commission=self.comm1, account=self.client_acc_1, comm_profile=self.comm_profile1
        ).send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(
            commission=self.comm2, account=self.client_acc_2, comm_profile=self.comm_profile2
        ).send_post_request()
        time.sleep(3)
        # endregion

        # region Step 1 - Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Comparing Status of DMA order",
        )
        # endregion

        # region Step 1 - Trade DMA order
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        class_name.print_message("TRADE", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.TransStatus.value: "TER",
            },
            execution_report_message,
            "Comparing TransExecStatus after Execute DMA",
        )
        # endregion

        # region Step 2 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "400",
                "AvgPx": "20",
                "SettlCurrAmt": "400",
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)

        order_update_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update_reply,
            "Comparing PostTradeStatus after Book",
        )

        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id = alloc_report_reply["ClientAllocID"]
        # endregion

        # region Step 3 - Approve block
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        class_name.print_message("APPROVE", responses)
        # endregion

        # region Step 3 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        list_of_security_account = [self.client_acc_1, self.client_acc_2]
        for account in list_of_security_account:
            self.confirmation_request.update_fields_in_component(
                "ConfirmationBlock",
                {
                    "AllocAccountID": account,
                    "AllocQty": self.qty_to_alloc,
                    "AvgPx": self.price,
                },
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            class_name.print_message(f"CONFIRMATION FOR {account}", responses)

            conf_report_reply = self.java_api_manager.get_last_message(
                ORSMessageType.ConfirmationReport.value
            ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]

            expected_commissions: dict = {
                JavaApiFields.CommissionRate.value: "5.0",
                JavaApiFields.CommissionAmount.value: "10.0",
                JavaApiFields.CommissionCurrency.value: "EUR",
                JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
                JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_PCT.value,
            }
            if conf_report_reply["AllocAccountID"] == "CLIENT_COMM_1_SA2":
                expected_commissions.update(
                    {JavaApiFields.CommissionRate.value: "10.0", JavaApiFields.CommissionAmount.value: "1.0"}
                )
            self.java_api_manager.compare_values(
                expected_commissions,
                conf_report_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
                f"Comparing Client Commission for {account}",
            )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
