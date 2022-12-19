import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7475(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        exec_price = '2'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        orders_id = list()
        # endregion

        # region_create_orders(precondition)
        for i in range(3):
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'AccountGroupID': client_name,
                'OrdQty': qty,
                "ClOrdID": bca.client_orderid(9),
                'Price': price,
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message('Create CO order', responses)
            orders_id.append(self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                                 JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
        # endregion

        # region mass manual execution and  verify expected result(step 1 )
        exec_ids = []
        for order in orders_id:
            self.trade_entry_request.set_default_trade(order, exec_price, qty)
            responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
            print_message(f'Trade CO order {order}', responses)
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            exec_ids.append(execution_report['ExecID'])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, 'Check ExecSts from step 1')
        # endregion

        # region step 2 - Complete CO orders
        orders_id_block = []
        for order in orders_id:
            orders_id_block.append({JavaApiFields.OrdID.value: order})
        self.complete_request.set_default(self.data_set)
        self.complete_request.update_fields_in_component('DFDManagementBatchBlock', {
            "DFDOrderList": {"DFDOrderBlock": orders_id_block}})
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request,
                                                                            {'OrdID': orders_id[0],
                                                                             'OrdID_2': orders_id[1],
                                                                             'OrdID_3': orders_id[2]})
        print_message('Complete all CO orders', responses)
        for order in orders_id:
            order_reply = \
                self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value, order).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
                order_reply, 'Check expected and actually result from step 2')

        # endregion

        # region step 3 - Bulk Booking CO orders
        self.allocation_instruction.set_default_book(orders_id[0])
        gross_trade_amt = float(exec_price) * float(qty)
        bulk_qty = str(float(qty) * 3)
        exec_alloc_block_list = []
        for exec_id in exec_ids:
            exec_alloc_block_list.append(
                {"ExecQty": qty, "ExecID": exec_id, "ExecPrice": exec_price})
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   "ExecAllocList": {
                                                                       "ExecAllocBlock": exec_alloc_block_list},
                                                                   "AllocInstructionID": "0",
                                                                   "AllocTransType": "New",
                                                                   "AllocType": "ReadyToBook",
                                                                   "Qty": bulk_qty,
                                                                   "GrossTradeAmt": gross_trade_amt,
                                                                   "BookingType": "RegularBooking",
                                                                   "AvgPx": exec_price,
                                                                   "AccountGroupID": client_name,
                                                                   "ErroneousTrade": "No",
                                                                   "NetGrossInd": "Gross",
                                                                   "SettlCurrAmt": gross_trade_amt,
                                                                   "OrdAllocList": {
                                                                       "OrdAllocBlock": orders_id_block}
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message('Book CO orders', responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report, 'Check actually and expected result from step 3')
        # endregion

        # region step 4
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                             {
                                                                 "ConfirmationID": "0",
                                                                 "AllocAccountID": self.data_set.get_account_by_name(
                                                                     'client_pt_1_acc_1'),
                                                                 "ConfirmTransType": "NEW",
                                                                 "ConfirmType": "CON",
                                                                 "AllocQty": bulk_qty,
                                                                 "AvgPx": exec_price,
                                                                 "NetMoney": gross_trade_amt,
                                                             })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message('Allocate block', responses)
        allocation_report = \
        self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report,
            'Check Status ,MatchStatus and Summary Status (part of step 4)')
        confirmation_report = \
        self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AllocQty.value: bulk_qty}, confirmation_report,
                                             'Check Qty (part of step 4)')
        # endregion
