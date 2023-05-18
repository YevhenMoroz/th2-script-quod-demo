import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import (
    FixMessageAllocationInstructionReportOMS,
)
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    ExecutionReportConst,
    JavaApiFields,
    SubmitRequestConst,
    OrderReplyConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T9155(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "2954.7989"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create Market Care order
        self.submit_request.set_default_care_market(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock", {"OrdQty": self.qty, "AccountGroupID": self.client}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Create Market Care order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id: str = order_reply["OrdID"]
        cl_ord_id: str = order_reply["ClOrdID"]

        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
            },
            order_reply,
            "Step 1 - Checking Status of Market Care order",
        )
        # endregion

        # region Step 2 - Manual execute Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request, {ord_id: ord_id})
        print_message("Execute", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        exec_id: str = exec_report["ExecID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.AvgPrice.value: self.price,
                JavaApiFields.ExecPrice.value: self.price,
            },
            exec_report,
            "Step 2 - Checking Status, AvgPrice after execution",
        )
        # endregion

        # region Step 3 - Complete and Book
        # Complete
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order, {ord_id: ord_id})
        print_message("COMPLETE", responses)
        exec_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id_calculated: str = exec_report_reply["ExecID"]

        # Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "Qty": self.qty,
                "AccountGroupID": self.client,
                "GrossTradeAmt": "295479",
                "AvgPx": self.price,
                "SettlCurrAmt": "295479",
                "ExecAllocList": {
                    "ExecAllocBlock": [{"ExecQty": self.qty, "ExecID": exec_id, "ExecPrice": self.price}]
                },
                "CalculatedExecList": {"ExecAllocBlock": [{"ExecQty": self.qty, "ExecID": exec_id_calculated}]},
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(
            self.allocation_instruction, {ord_id: ord_id}
        )
        print_message("BOOK", responses)

        # Checking Order_OrdUpdate
        order_update_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update_reply,
            "Step 3 - Checking PostTradeStatus after Book",
        )
        # endregion

        # region Step 4 - Check Allocation Report 35=J
        list_of_ignored_fields: list = ["TransactTime", "QuodTradeQualifier", "BookID", "SettlDate", "Currency",
                                        "NetMoney", "TradeDate", "BookingType", "NoParty", "AllocInstructionMiscBlock1",
                                        "ExecAllocGrp", "tag5120", "Instrument", "RootSettlCurrAmt", "GrossTradeAmt",
                                        "AllocID"]
        change_parameters = {
            "AllocType": "5",
            "Quantity": self.qty,
            "Side": "1",
            "AvgPx": self.price,
            "ReportedPx": self.price,
            "AllocTransType": "0",
            "NoOrders": [{"ClOrdID": cl_ord_id, "OrderID": ord_id, "OrderAvgPx": self.price}],
        }
        self.alloc_report.change_parameters(change_parameters)
        self.fix_verifier_dc.check_fix_message_fix_standard(
            self.alloc_report,
            key_parameters=["NoOrders", "AllocType", "AllocTransType"],
            ignored_fields=list_of_ignored_fields,
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
