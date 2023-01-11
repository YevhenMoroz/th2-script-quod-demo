import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionReportConst
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


class QAP_T7305(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        order_ids_list = []
        # region create CO orders step 1
        for i in range(2):
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'AccountGroupID': self.client,
                'OrdQty': self.qty,
                "ClOrdID": bca.client_orderid(9),
                'Price': self.price,
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message('Create CO order', responses)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            order_ids_list.append(order_reply[JavaApiFields.OrdID.value])
            cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Check expected and actually results from step 1')

        # endregion

        # trade CO orders step 2
        list_of_exec_id = []
        for order_id in order_ids_list:
            for i in range(2):
                self.trade_entry.set_default_trade(order_id, self.price, str(float(self.qty) / 2))
                self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.venue})
                responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
                print_message(f'Trade CO  order {order_id}', responses)
                actually_result = \
                    self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                        JavaApiFields.ExecutionReportBlock.value]
                list_of_exec_id.append(actually_result[JavaApiFields.ExecID.value])
        # endregion

        # region step 3 Canceled executions
        self.trade_entry.remove_fields_from_component('TradeEntryRequestBlock', ['LastMkt'])
        for order_id in order_ids_list:
            self.trade_entry.set_default_cancel_execution(order_id, list_of_exec_id[
                order_ids_list.index(order_id) + order_ids_list.index(order_id)])
            responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
            print_message(
                f'Cancel execution {list_of_exec_id[order_ids_list.index(order_id) + order_ids_list.index(order_id)]} of {order_id} order',
                responses)
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
                execution_report, 'Check Expected and Actually results from step 3')
        # endregion

        # region step 4 and step 5
        # Complete orders (part of step 4)
        self.complete_request.set_default_complete_for_some_orders(order_ids_list)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request,
                                                                            filter_dict={'OrderID': order_ids_list[0],
                                                                                         'OrderID2': order_ids_list[1]})
        print_message(f'Complete CO orders {order_ids_list}', responses)
        # end of part

        # Mass Book orders (part of step 4)
        # mass book (part of step 4)
        gross_trade_amt = str(float(self.qty) / 2 * float(self.price))
        for order_id in order_ids_list:
            self.allocation_instruction.set_default_book(order_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
                "AccountGroupID": self.client,
                "SettlCurrAmt": gross_trade_amt,
                'Qty': str(float(self.qty) / 2),
                'ExecAllocList': {
                    'ExecAllocBlock': [{'ExecQty': str(float(self.qty) / 2),
                                        'ExecID': list_of_exec_id[
                                            order_ids_list.index(order_id) + order_ids_list.index(order_id) + 1],
                                        'ExecPrice': self.price}]},
                "ComputeFeesCommissions": "No"
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
            print_message(f'Book {order_id} order', responses)

            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[JavaApiFields.OrdUpdateBlock.value]
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]

            # Check expected and actually results (part of step 4)
            self.java_api_manager.compare_values({JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
                                                 order_update, f'Check Expected and Actually PostTradeStatus  for {order_id} (step 4)')
            # end of part

            # Check expected and actually results (part of step 5)
            self.java_api_manager.compare_values({JavaApiFields.Qty.value: str(float(self.qty) / 2)},
                                                 allocation_report, f'Check Expected and Actually Qty for block'
                                                                    f'{allocation_report[JavaApiFields.ClientAllocID.value]} (step 5)')
            # end of part
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
