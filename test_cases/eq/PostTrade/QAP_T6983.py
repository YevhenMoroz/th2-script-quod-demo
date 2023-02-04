import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionReportConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6983(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client('client_pt_1')
        self.qty = '100'
        self.price = '10'
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.modification_request = OrderModificationRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : Create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Check expected and actually results form step 1')
        ord_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region step 2 : Split CO order
        half_qty = str(float(self.qty) / 2)
        self.order_submit.set_default_child_dma(ord_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'OrdQty': half_qty,
            'Price': self.price,
            "ClOrdID": bca.client_orderid(9),
            'ExecutionPolicy': 'DMA'
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply_child = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id_first_child_dma_order = order_reply_child[JavaApiFields.OrdID.value]
        # endregion

        # region step 3 : Execute Child DMA order
        self.execution_report.set_default_trade(order_id_first_child_dma_order)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "OrdQty": half_qty,
                                                             "Side": "Buy",
                                                             "LastTradedQty": half_qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "LeavesQty": "0.0",
                                                             "CumQty": half_qty,
                                                             "AvgPrice": self.price
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {'ParentOrderID': ord_id,
                                                                                        'ChildOrderID': order_id_first_child_dma_order})
        execution_report_of_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                              f"'{JavaApiFields.OrdID.value}': "
                                                                              f"'{ord_id}'").get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        first_exec_id_parent_order = execution_report_of_co_order[JavaApiFields.ExecID.value]
        execution_report_of_dma_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                               f"'{JavaApiFields.OrdID.value}': "
                                                                               f"'{order_id_first_child_dma_order}'").get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id_dma = execution_report_of_dma_order[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value},
            execution_report_of_dma_order, 'Check expected and actually results from step 3')
        # endregion

        # region step 4 : Manual Execute CO order
        self.trade_entry.set_default_trade(ord_id, self.price, half_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_report_of_co_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value
            ]
        second_exec_id_parent_order = execution_report_of_co_order[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report_of_co_order, 'Check that CO order fully filled (step 4)')
        # endregion

        # region step 5
        # part 1: complete CO order
        self.complete_message.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        # end of part

        # part 2: book CO order
        self.allocation_instruction.set_default_book(ord_id)
        gross_trade_amt = float(self.qty) * float(self.price)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": self.qty,
                                                                "AvgPx": self.price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}, order_update,
            'Check expected and actually results for order (step 5)')
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report, 'Check expected and actually results for block (step 5)')
        # end of part

        # endregion

        # region step 6
        order_report = OrdReportOMS(data_set=self.data_set)
        order_report.set_default_eliminated(order_id_first_child_dma_order, self.price)
        order_report.update_fields_in_component('OrdReportBlock', {
            "Side": "Buy",
            "OrdQty": str(half_qty),
            "CumQty": str(half_qty),
            "LeavesQty": "0.0",
        })
        self.java_api_manager.send_message_and_receive_response(order_report)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_ELI.value},
                                             order_reply,
                                             'Check expected and actually results for Child DMA order (step 6)')

        # part of step 6 : Check Statuses of parent order
        self.modification_request.set_default(self.data_set, ord_id)
        self.modification_request.update_fields_in_component('OrderModificationRequestBlock',
                                                             {'Price': self.price,
                                                              'OrdQty': self.qty,
                                                              'AccountGroupID': self.client,
                                                              'PosValidity': 'DEL',
                                                              'WashBookAccountID': self.data_set.get_washbook_account_by_name(
                                                                  'washbook_account_2')}
                                                             )
        self.java_api_manager.send_message_and_receive_response(self.modification_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}, order_reply,
            'Check expected and actually results for parent order (step 6)')
        # end of part

        # part of step 6 check statuses of block
        list_of_executions_of_co_order = [first_exec_id_parent_order, second_exec_id_parent_order]
        self.allocation_instruction.set_ament_book_with_multiply_execution(alloc_id, list_of_executions_of_co_order,
                                                                           half_qty, self.price)
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report, 'Check expected and actually results for block (step 6)')
        # end of part

        # endregion
