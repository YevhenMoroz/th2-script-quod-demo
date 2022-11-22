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


class QAP_T7231(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "20"
        self.per_u_qty = self.data_set.get_comm_profile_by_name("per_u_qty")
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
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
        class_name = QAP_T7231
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        # send commission
        self.rest_commission_sender.set_modify_client_commission_message(
            client=self.client, comm_profile=self.per_u_qty
        )
        self.rest_commission_sender.send_post_request()
        time.sleep(3)

        # send fees
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.perc_amt)
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_1")})
        self.rest_commission_sender.send_post_request()
        time.sleep(3)
        # endregion

        # region Precondition - Create Care order
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
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Comparing Status of Care order",
        )
        # endregion

        # region Precondition - Execution of Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        class_name.print_message("EXECUTE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            "Comparing Execution status (TransExecStatus)",
        )

        # Checking Commission
        expected_commissions: dict = {
            JavaApiFields.CommissionRate.value: "0.5",
            JavaApiFields.CommissionAmount.value: "50.0",
            JavaApiFields.CommissionCurrency.value: "EUR",
            JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_UNI.value,
        }
        self.java_api_manager.compare_values(
            expected_commissions,
            exec_report["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Checking Client Commission after Execute",
        )

        # Checking Fees
        expected_fees: dict = {
            JavaApiFields.MiscFeeType.value: "EXC",
            JavaApiFields.MiscFeeAmt.value: "100.0",
            JavaApiFields.MiscFeeBasis.value: "P",
            JavaApiFields.MiscFeeCurr.value: "EUR",
            JavaApiFields.MiscFeeRate.value: "5.0",
        }
        self.java_api_manager.compare_values(
            expected_fees,
            exec_report["MiscFeesList"]["MiscFeesBlock"][0],
            "Checking Fees after Execute",
        )
        # endregion

        # region Precondition - Complete CO
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

        # region Step 1-3 - Open Split Book and Change rate of Commissions and Fees > Split Booking
        self.allocation_instruction.set_default_book(ord_id)

        expected_commissions_after_amend: dict = {
            JavaApiFields.CommissionRate.value: "1.0",
            JavaApiFields.CommissionAmount.value: "100.0",
            JavaApiFields.CommissionCurrency.value: "EUR",
            JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_UNI.value,
        }
        expected_fees_after_amend: dict = {
            JavaApiFields.RootMiscFeeType.value: "EXC",
            JavaApiFields.RootMiscFeeAmt.value: "200.0",
            JavaApiFields.RootMiscFeeBasis.value: "P",
            JavaApiFields.RootMiscFeeCurr.value: "EUR",
            JavaApiFields.RootMiscFeeRate.value: "10.0",
        }

        self.allocation_instruction.update_fields_in_component(
            "AllocationInstructionBlock",
            {
                "AccountGroupID": self.client,
                "ClientCommissionList": {"ClientCommissionBlock": [expected_commissions_after_amend]},
                "RootMiscFeesList": {"RootMiscFeesBlock": [expected_fees_after_amend]},
                "AllocationInstructionQtyList": {
                    "AllocationInstructionQtyBlock": [
                        {
                            "BookingQty": "25",
                            "NetGrossInd": "Gross",
                            "BookingType": "RegularBooking",
                            "SettlDate": datetime.utcnow().isoformat(),
                            "GrossTradeAmt": "500",
                            "NetMoney": "575",
                        },
                        {
                            "BookingQty": "75",
                            "NetGrossInd": "Gross",
                            "BookingType": "RegularBooking",
                            "SettlDate": datetime.utcnow().isoformat(),
                            "GrossTradeAmt": "1500",
                            "NetMoney": "1725",
                        },
                    ]
                },
                "GrossTradeAmt": "2000",
                "AvgPx": "20",
                "SettlCurrAmt": "2300",
            },
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message("BOOK", responses)
        # endregion

        # region Step 4 - Checking Client Commission and Fees for first and second block
        # AllocationReport for 1st block
        alloc_report_message_first = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value, filter_value="'Qty': '25.0'"
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        # alloc_id = alloc_report_message["ClientAllocID"]

        # Comparing Client Commission for 1st block
        expected_commissions_after_amend[JavaApiFields.CommissionAmount.value] = "25.0"
        self.java_api_manager.compare_values(
            expected_commissions_after_amend,
            alloc_report_message_first["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Book for 1st block",
        )

        # Comparing Fees for 1st block
        expected_fees_after_amend[JavaApiFields.RootMiscFeeAmt.value] = "50.0"
        self.java_api_manager.compare_values(
            expected_fees_after_amend,
            alloc_report_message_first["RootMiscFeesList"]["RootMiscFeesBlock"][0],
            "Comparing Fees after Book for 1st block",
        )

        # AllocationReport for 2nd block
        alloc_report_message_second = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value, filter_value="'Qty': '75.0'"
        ).get_parameters()[JavaApiFields.AllocationReportBlock.value]

        # Comparing Client Commission for 2nd block
        expected_commissions_after_amend[JavaApiFields.CommissionAmount.value] = "75.0"
        self.java_api_manager.compare_values(
            expected_commissions_after_amend,
            alloc_report_message_second["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Client Commission after Book for 2nd block",
        )

        # Comparing Fees for 2nd block
        expected_fees_after_amend[JavaApiFields.RootMiscFeeAmt.value] = "150.0"
        self.java_api_manager.compare_values(
            expected_fees_after_amend,
            alloc_report_message_second["RootMiscFeesList"]["RootMiscFeesBlock"][0],
            "Comparing Fees after Book for 2nd block",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
