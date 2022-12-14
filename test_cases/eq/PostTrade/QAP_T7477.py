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
from test_framework.java_api_wrappers.java_api_constants import AllocationReportConst, JavaApiFields, \
    ExecutionReportConst, OrderReplyConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.read_log_wrappers.ReadLogVerifier import ReadLogVerifier
from test_framework.read_log_wrappers.oms_messages.AlsMessages import AlsMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

seconds, nanos = timestamps()  # Test case start time


class QAP_T7477(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.read_log_conn = self.environment.get_list_read_log_environment()[0].read_log_conn
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.compute_booking_fees_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.read_log_verifier = ReadLogVerifier(self.read_log_conn, self.test_id)
        self.currency = self.data_set.get_currency_by_name('currency_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        new_price = '20'
        account_first = self.data_set.get_account_by_name('client_pt_1_acc_1')
        account_second = self.data_set.get_account_by_name('client_pt_1_acc_2')
        client = self.data_set.get_client_by_name('client_pt_1')
        # region precondition

        # part 1 : Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        # end of part

        # part 2 (trade dma order)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": price,
                "AvgPrice": price,
                "LastPx": price,
                "OrdQty": qty,
                "LastTradedQty": qty,
                "CumQty": qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value, },
            execution_report_message,
            "Comparing ExecSts after Execute DMA (part of precondition)")
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value, },
            order_reply,
            "Comparing PostTradeStatus after Execute DMA (part of precondition)", )
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # end of part

        # endregion

        # region step 1 and step 2
        gross_trade_amt = float(price) * float(qty)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": qty,
                                                                "AvgPx": price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': price}]},
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        alloc_instr_id = allocation_report[JavaApiFields.ClBookingRefID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report,
            'Check expected and actually results for block (step 2)')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, 'Check expected and actually result for order (step 2)')
        # endregion

        # region step 3
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            allocation_report,
            'Check expected and actually results (step 3)')
        # endregion

        # region step 4 and step 5
        list_of_confirmation_id = []
        qty_of_allocation = str(float(qty) / 2)
        list_of_account = [account_first, account_second]
        for account in list_of_account:
            self.confirmation_request.set_default_allocation(alloc_id)
            self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                                 {"AllocQty": qty_of_allocation,
                                                                  "Side": "B",
                                                                  "AvgPx": price,
                                                                  "AllocAccountID": account})
            self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            list_of_confirmation_id.append(confirmation_report[JavaApiFields.ConfirmationID.value])
        # endregion

        # region step 6 Check ALS logs Status New
        als_message = AlsMessages.execution_report.value
        trade_date = datetime.now().strftime('%Y-%m-%d')
        als_message.update(
            {"ConfirmStatus": "New", "ClientAccountID": account_first, "AllocQty": "100", "TradeDate": trade_date})
        self.read_log_verifier.check_read_log_message(als_message, ["ConfirmStatus", 'ClientAccountID', 'TradeDate'],
                                                      timeout=50000)
        # endregion

        # region step 7 (amend allocation)
        time.sleep(3)
        self.confirmation_request.set_default_amend_allocation(list_of_confirmation_id[0], alloc_id, new_price,
                                                               qty_of_allocation)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            'AllocAccountID': account_first
        })
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AvgPx.value: str(float(new_price))},
            confirmation_report,
            'Check expected and actually results (part of step 7)')
        # endregion

        # region step 8 Check ALS logs Status "Replace"
        als_message.update({"ConfirmStatus": "Replace"})
        self.read_log_verifier.check_read_log_message(als_message, ["ConfirmStatus", 'ClientAccountID', 'TradeDate'],
                                                      timeout=60000)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
