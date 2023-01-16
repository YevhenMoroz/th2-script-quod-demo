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
    OrderReplyConst,
    JavaApiFields,
    CommissionAmountTypeConst,
    CommissionBasisConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import (
    ComputeBookingFeesCommissionsRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8382(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "20"
        self.abs_amt_gbp_small = self.data_set.get_comm_profile_by_name("abs_amt_gbp_small")
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")  # CLIENT_COMM_1_SA1
        self.currency = self.data_set.get_currency_by_name("currency_3")  # GBp
        self.comm_currency = self.data_set.get_currency_by_name("currency_2")  # GBP
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.order_modification_request = OrderModificationRequest()
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T8382
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(
            client=self.client, comm_profile=self.abs_amt_gbp_small
        )
        self.rest_commission_sender.change_message_params(
            {"venueID": self.data_set.get_venue_by_name("venue_2"), "executionPolicy": "D", "side": "B"}
        )
        self.rest_commission_sender.send_post_request()
        time.sleep(3)
        # endregion

        # region Step 1 - Create DMA order
        self.submit_request.set_default_dma_limit()
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "SettlCurrency": self.currency,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
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
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Comparing Status of DMA order",
        )
        # endregion

        # region Step 2 - Execute DMA order
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_3"),
                "LastMkt": self.data_set.get_mic_by_name("mic_2"),
                "Currency": self.currency,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        class_name.print_message("EXECUTE DMA", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        ord_id = execution_report_message["OrdID"]
        cl_ord_id = execution_report_message["ClOrdID"]
        exec_id = execution_report_message["ExecID"]
        post_trd_sts = execution_report_message["PostTradeStatus"]
        # endregion

        # region Step 3 - Comparing Commissions
        expected_commission: dict = {
            JavaApiFields.CommissionRate.value: "0.01",
            JavaApiFields.CommissionAmount.value: "0.01",
            JavaApiFields.CommissionCurrency.value: self.comm_currency,
            JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_ABS.value,
        }
        self.java_api_manager.compare_values(
            expected_commission,
            execution_report_message["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Commissions",
        )
        # endregion

        # region Step 4-5 - Open Booking ticket and Checking Commissions
        self.compute_request.set_list_of_order_alloc_block(cl_ord_id, ord_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(client=self.client)
        # self.compute_request.update_fields_in_component()
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_request)
        class_name.print_message("OPEN BOOKING TICKET", responses)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value
        ).get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        self.java_api_manager.compare_values(
            expected_commission,
            compute_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Commissions in Booking ticket",
        )
        # endregion

        # region Step 5 - Book order
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client,
                "ClientCommissionList": {"ClientCommissionBlock": [expected_commission]},
                "Currency": self.comm_currency,
                "GrossTradeAmt": "20",
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "AvgPx": "0.2",
                "SettlCurrAmt": "20.01",
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)

        alloc_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        alloc_id = alloc_report_reply["ClientAllocID"]
        self.java_api_manager.compare_values(
            expected_commission,
            alloc_report_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Book",
        )
        # endregion

        # region Step 7 - Approve block
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        class_name.print_message("APPROVE", responses)
        # endregion

        # region Step 7 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.account,
                "AllocQty": self.qty,
                "AvgPx": "0.2",
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message("ALLOCATE", responses)

        conf_report_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            expected_commission,
            conf_report_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Allocate",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
