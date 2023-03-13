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
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7415(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "10"
        self.bas_amt = self.data_set.get_comm_profile_by_name("bas_amt")
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")  # CLIENT_COMM_1_SA1
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
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
        class_name = QAP_T7415
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client, comm_profile=self.bas_amt)
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
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        ord_id = order_reply.get_parameter("OrdReplyBlock")["OrdID"]
        cl_ord_id = order_reply.get_parameter("OrdReplyBlock")["ClOrdID"]
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of Care order",
        )
        # endregion

        # region Step 2 - Execution of Care order
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
        self.java_api_manager.compare_values(
            {"CommissionRate": "1.0", "CommissionAmount": "0.1"},
            exec_report["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission",
        )
        # endregion

        # region Step 3 - Complete CO
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        class_name.print_message("COMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {
                "PostTradeStatus": OrderReplyConst.PostTradeStatus_RDY.value,
                "DoneForDay": OrderReplyConst.DoneForDay_YES.value,
            },
            order_reply,
            "Comparing values after Complete",
        )
        # endregion

        # region Step 5 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client,
                "ClientCommissionList": {
                    "ClientCommissionBlock": [
                        {
                            "CommissionAmountType": CommissionAmountTypeConst.CommissionAmountType_BRK.value,
                            "CommissionAmount": "0.1",
                            "CommissionBasis": "BPS",
                            "CommissionCurrency": self.data_set.get_currency_by_name("currency_1"),  # EUR
                            "CommissionRate": "1",
                        }
                    ]
                },
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)

        alloc_report_message = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        alloc_id = alloc_report_message.get_parameter("AllocationReportBlock")["ClientAllocID"]
        client_comm = alloc_report_message.get_parameter("AllocationReportBlock")["ClientCommissionDataBlock"][
            "ClientCommission"
        ]
        self.java_api_manager.compare_values(
            {"ClientCommission": "0.1"}, {"ClientCommission": client_comm}, "Comparing Client Commission after Book"
        )
        # endregion

        # region Step 6 - Approve block
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message("APPROVE", responses)
        # endregion

        # region Step 6 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.account,
                "AllocQty": self.qty,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message("ALLOCATE", responses)

        # Comparing values for Allocation after Allocate block
        conf_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()["ConfirmationReportBlock"]
        self.java_api_manager.compare_values(
            {"ClientCommission": "0.1"},
            {"ClientCommission": conf_report_message["ClientCommissionDataBlock"]["ClientCommission"]},
            "Comparing Client Commission after Allocate block",
        )
        self.rest_commission_sender.clear_commissions()
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
