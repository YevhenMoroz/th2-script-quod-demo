import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionReportConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateBatchRequest import BlockUnallocateBatchRequest
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusBatchRequest import \
    ForceAllocInstructionStatusBatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T6965(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty_first = "100"
        self.qty_second = "200"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account_1 = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.alloc_account_2 = self.data_set.get_account_by_name("client_pt_1_acc_2")  # MOClient_SA2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.mass_unallocate = BlockUnallocateBatchRequest()
        self.approve_blocks = ForceAllocInstructionStatusBatchRequest()
        self.confirmation_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO orders via JavaApi:
        list_of_qty = [self.qty_first, self.qty_second]
        list_of_sec_account = [self.alloc_account_1, self.alloc_account_2]
        dict_orders_id = {}
        list_of_orders_ids = []
        for qty in list_of_qty:
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'AccountGroupID': self.client,
                'OrdQty': qty,
                'Price': self.price,
                "ClOrdID": bca.client_orderid(9)
            })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                                 order_reply, 'Checking expected and actually results  (step 1)')
            list_of_orders_ids.append(order_reply[JavaApiFields.OrdID.value])
        # endregion

        # region step 2 : Execute CO orders
        list_of_exec_id = []
        for order_id in list_of_orders_ids:
            dict_orders_id.update({order_id: order_id})
            qty = list_of_qty[list_of_orders_ids.index(order_id)]
            self.trade_entry.set_default_trade(order_id, self.price, qty)
            self.java_api_manager.send_message_and_receive_response(self.trade_entry)
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            list_of_exec_id.append(execution_report[JavaApiFields.ExecID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, f'Checking expected and actually results for {order_id} order (step 2)')
        # endregion

        # region step 3 : Complete CO orders
        self.complete_message.set_default_complete_for_some_orders(list_of_orders_ids)
        self.java_api_manager.send_message_and_receive_response(self.complete_message, dict_orders_id)
        for order_id in list_of_orders_ids:
            order_reply = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                 JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                order_reply,
                f'Checking expected and actually results for {order_id} order (step 3)')
        # endregion

        # region step 4
        list_of_alloc_instruction_ids = []
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        for order_id in list_of_orders_ids:
            qty = list_of_qty[list_of_orders_ids.index(order_id)]
            self.allocation_instruction.set_default_book(order_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
                "AccountGroupID": self.client,
                'Side': 'Buy',
                "Qty": qty,
                'InstrID': instrument_id,
                "ComputeFeesCommissions": "Yes"
            })
            if list_of_orders_ids.index(order_id) == 0:
                self.allocation_instruction.remove_fields_from_component('AllocationInstructionBlock',
                                                                         ["NetGrossInd",
                                                                          "SettlCurrAmt",
                                                                          "AvgPx", 'BookingType',
                                                                          'GrossTradeAmt',
                                                                          'Currency',
                                                                          'RecomputeInSettlCurrency'
                                                                          ])
            self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            list_of_alloc_instruction_ids.append(allocation_report[JavaApiFields.ClientAllocID.value])
            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
                 JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                order_update, f'Checking expected and actually results for {order_id} order (step 4)')
        # endregion

        # region step 5: Mass Approve
        filter_dict = {}
        self.approve_blocks.set_default(list_of_alloc_instruction_ids)
        self.java_api_manager.send_message_and_receive_response(self.approve_blocks,
                                                                {'AllocID': list_of_alloc_instruction_ids[0],
                                                                 'AllocID2': list_of_alloc_instruction_ids[1]})
        for alloc_id in list_of_alloc_instruction_ids:
            filter_dict.update({alloc_id:alloc_id})
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, alloc_id).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                 JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_MAN.value},
                allocation_report, f'Checking expected and actually results for {alloc_id} block (step 5)')
        # endregion

        # region step 6 allocate blocks
        for alloc_id in list_of_alloc_instruction_ids:
            self.confirmation_request.set_default_allocation(alloc_id)
            self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
                "AllocAccountID": list_of_sec_account[list_of_alloc_instruction_ids.index(alloc_id)],
                'AllocQty': list_of_qty[list_of_alloc_instruction_ids.index(alloc_id)],
                'AvgPx': self.price,
            })
            self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value},
                confirmation_report,
                f'Checking expected and actually results for allocation of block {alloc_id} (step 6)')
            allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                 JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value,
                 JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_MAN.value
                 }, allocation_report, f'Checking expected and actually results for block {alloc_id} (step 6)')
        # endregion

        # region step 7
        self.mass_unallocate.set_default(list_of_alloc_instruction_ids)
        self.java_api_manager.send_message_and_receive_response(self.mass_unallocate, filter_dict)
        for alloc_id in list_of_alloc_instruction_ids:
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                 JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_MAN.value},
                allocation_report,
                f'Checking expected and actually result for block with {alloc_id} (step 7)')
            self.java_api_manager.key_is_absent(JavaApiFields.AllocSummaryStatus.value, allocation_report,
                                                f'Checking that {JavaApiFields.AllocSummaryStatus.value} is '
                                                f'empty for block {alloc_id}')
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_CXL.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
                confirmation_report,
                f'Checking expected and actually result for allocation of block {alloc_id} (step 7)')
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
