import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.MassConfirmationOMS import MassConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateBatchRequest import BlockUnallocateBatchRequest
from test_framework.java_api_wrappers.ors_messages.ForceAllocInstructionStatusBatchRequest import \
    ForceAllocInstructionStatusBatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



class QAP_T7359(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.mass_single_allocation = MassConfirmationOMS()
        self.mass_unallocate = BlockUnallocateBatchRequest()
        self.approve_blocks = ForceAllocInstructionStatusBatchRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity)
        qty = '5000'
        price = '10'
        alloc_account = self.data_set.get_account_by_name('client_pt_7_acc_1')
        client = self.data_set.get_client_by_name('client_pt_8')
        # endregion

        # region create 2 DMA order and execute them (step 1 step 2 and step 3)
        # part 1 : Create DMA orders
        list_of_order_ids = []
        for i in range(2):
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component(
                "NewOrderSingleBlock",
                {"OrdQty": qty,
                 "AccountGroupID": client,
                 "Price": price,
                 "ClOrdID": bca.client_orderid(9)})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            list_of_order_ids.append(order_reply[JavaApiFields.OrdID.value])
        # end of part

        # part 2: Trade DMA orders
        for ord_id in list_of_order_ids:
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
        # end of part

        # endregion

        # region mass book orders (step 4)
        list_of_alloc_instruction_ids = []
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        for order_id in list_of_order_ids:
            self.allocation_instruction.set_default_book(order_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
                "AccountGroupID": client,
                'Side': 'Buy',
                "Qty": qty,
                'InstrID': instrument_id,
                "ComputeFeesCommissions": "Yes"
            })
            if list_of_order_ids.index(order_id) == 0:
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
        # endregion

        # region step 5: Mass approve
        self.approve_blocks.set_default(list_of_alloc_instruction_ids)
        self.java_api_manager.send_message_and_receive_response(self.approve_blocks,
                                                                {'AllocID': list_of_alloc_instruction_ids[0],
                                                                 'AllocID2': list_of_alloc_instruction_ids[1]})
        for alloc_id in list_of_alloc_instruction_ids:
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
                allocation_report, f'Checking expected and actually results for {alloc_id} block (step 5)')
        # endregion

        # region step 6: Mass Single Allocate
        filter_dict = {}
        net_money = str(float(qty) * float(price))
        for alloc_id in list_of_alloc_instruction_ids:
            filter_dict.update({alloc_id: alloc_id})
            self.mass_single_allocation.set_instance_of_confirmation_list(alloc_id, alloc_account, instrument_id, qty,
                                                                          net_money, price)
        self.mass_single_allocation.set_default_confimations_new()
        self.java_api_manager.send_message_and_receive_response(self.mass_single_allocation, filter_dict)
        for alloc_id in list_of_alloc_instruction_ids:
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                 JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
                allocation_report,
                f'Checking expected and actually result for block with {alloc_id} (step 6)')
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value},
                confirmation_report,
                'Checking expected and actually result for allocation of block {alloc_id} (step 6)')
        # endregion

        # region step 7 : Mass Unallocate
        self.mass_unallocate.set_default(list_of_alloc_instruction_ids)
        self.java_api_manager.send_message_and_receive_response(self.mass_unallocate, filter_dict)
        for alloc_id in list_of_alloc_instruction_ids:
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                 JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
                allocation_report,
                f'Checking expected and actually result for block with {alloc_id} (step 7)')
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value,
                                                       alloc_id).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_CXL.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
                confirmation_report,
                'Checking expected and actually result for allocation of block {alloc_id} (step 7)')
        # endregion
