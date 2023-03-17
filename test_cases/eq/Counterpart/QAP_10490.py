import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusRequest import \
    ForceAllocInstructionStatusRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10490(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_4")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_4_acc_1")
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_4_venue_1")
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequest()
        self.confirmation = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region step 1: create DMA order
        self.new_order_single.set_default_dma_limit()
        qty = self.new_order_single.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.OrdQty.value]
        price = self.new_order_single.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        price = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {
                                                             'ClientAccountGroupID': self.client,
                                                             'PreTradeAllocationBlock': {
                                                                 'PreTradeAllocationList': {
                                                                     'PreTradeAllocAccountBlock': [{
                                                                         'AllocClientAccountID': self.account,
                                                                         'AllocQty': qty
                                                                     }]
                                                                 }
                                                             }
                                                         })
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(price))
            self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)

        agent_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_agent')
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order is created (step 1)')
        counterpart_block = order_reply[JavaApiFields.CounterpartList.value][JavaApiFields.CounterpartBlock.value]
        self.java_api_manager.compare_values({"CounterpartPresent": True},
                                             {'CounterpartPresent': agent_counterpart in counterpart_block},
                                             'Verify that Agent counterpart  present for order (step 1)')
        # endregion

        # region step 2: Execute and Book DMA order:
        # part 1: Execute DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_2"),
            "OrdQty": qty,
            "LastTradedQty": qty,
            "LastPx": price,
            "Price": price,
            "LeavesQty": 0,
            "CumQty": qty,
            "AvgPrice": price
        })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        # end_of_part

        # part 2: Book DMA order
        self.allocation_instruction.set_default_book(order_id)
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_2")
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"AccountGroupID": self.client,
                                                                'InstrID': instrument_id})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value). \
            get_parameters()[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value},
            allocation_report, 'Verifying that Block created (step 2)')
        counterpart_block = allocation_report[JavaApiFields.CounterpartList.value][JavaApiFields.CounterpartBlock.value]
        self.java_api_manager.compare_values({"CounterpartPresent": True},
                                             {'CounterpartPresent': agent_counterpart in counterpart_block},
                                             'Verify that Agent counterpart  present for block (step 2)')
        allocation_id = allocation_report[JavaApiFields.ClientAllocID.value]
        # endregion

        # region step 3: Approve and Allocate block:
        self.approve.set_default(allocation_id)
        self.java_api_manager.send_message(self.approve)
        self.confirmation.set_default_allocation(allocation_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.account,
            "InstrID": instrument_id})
        self.java_api_manager.send_message_and_receive_response(self.confirmation)
        confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        counterpart_block = confirmation_report[JavaApiFields.CounterpartList.value][JavaApiFields.CounterpartBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value},
            allocation_report, 'Verifying that confirmation created (step 3)')
        self.java_api_manager.compare_values({"CounterpartPresent": True},
                                             {'CounterpartPresent': agent_counterpart in counterpart_block},
                                             'Verify that Agent counterpart  present for confirmation (step 3)')
        # endregion
