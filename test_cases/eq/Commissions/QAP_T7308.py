import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import (
    ForceAllocInstructionStatusRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7308(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_3")  # MOClient3
        self.client_acc = self.data_set.get_account_by_name("client_pt_3_acc_1")  # MOClient3_SA1
        self.currency = self.data_set.get_currency_by_name("currency_3")  # GBp
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name("perc_amt"), client=self.client
        )
        self.rest_commission_sender.send_post_request()
        # endregion

        # region Step 1 - Create CO
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "AccountGroupID": self.client,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
                "SettlCurrency": self.currency,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value
        )["OrdID"]
        # endregion

        # region Step 2 - Execute order
        self.trade_request.set_default_trade(order_id, exec_price="20")
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        expected_result = {"TransExecStatus": "FIL"}
        self.java_api_manager.compare_values(expected_result, exec_reply, "Compare TransExecStatus")
        self.complete_message.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value
        ]
        alloc_id = alloc_report["AllocInstructionID"]
        # endregion

        # region Step 3 - Approve and Allocate order
        self.force_alloc.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.force_alloc)
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component(
            "ConfirmationBlock",
            {
                "AllocAccountID": self.client_acc,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "AvgPx": "0.2",
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        expected_result = {
            "CommissionCurrency": self.data_set.get_currency_by_name("currency_2"),
            "CommissionBasis": "PCT",
            "CommissionRate": "5.0",
            "CommissionAmount": "1.0",
            "CommissionAmountType": "BRK",
        }
        confirm_report = self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value
        ).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            expected_result,
            confirm_report["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Compare ClientCommission",
        )

        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
