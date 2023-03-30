import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    AllocationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T10497(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.qty = '300'
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : create DMA  order
        cd_ord_free_notes = 'QAP_T10497'
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.CDOrdFreeNotes.value: cd_ord_free_notes
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=20000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # endregion

        # region step 2: Trade DMA order and book its
        # part 1 : Fill DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             JavaApiFields.Side.value: "Buy",
                                                             JavaApiFields.LastTradedQty.value: self.qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: "Limit",
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.ExecType.value: "Trade",
                                                             JavaApiFields.TimeInForce.value: "Day",
                                                             JavaApiFields.LeavesQty.value: '0',
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        # end_of_part

        # part 2: Book DMA order
        self.allocation_instruction.set_default_book(order_id)
        back_office_notes = 'QAP_T10497_BACKOFFICE'
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   JavaApiFields.AvgPx.value: self.price,
                                                                   JavaApiFields.Qty.value: self.qty,
                                                                   JavaApiFields.BackOfficeNotes.value: back_office_notes,
                                                                   JavaApiFields.CDOrdFreeNotes.value: cd_ord_free_notes
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        self.java_api_manager.compare_values({JavaApiFields.BackOfficeNotes.value: back_office_notes,
                                              JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                                              JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_UNM.value},
                                             allocation_report,
                                             f'Verifying that block  created and has {JavaApiFields.BackOfficeNotes.value} field (step 2)')
        # end of part

        # part 3: Check 35=J (626 = 5 message)
        list_of_ignored_fields = ['NoParty', 'Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'IndividualAllocID', 'AllocNetPrice',
                                  'AllocPrice', 'Instrument']
        change_parameters = {'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': '*',
        }], 'AllocType': 5,
            'BackOfficeNote': back_office_notes,
            'Text': cd_ord_free_notes
        }
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        allocation_report.change_parameters({'BackOfficeNote': back_office_notes,
                                             'Text': cd_ord_free_notes})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report,
                                                         key_parameters=['ClOrdID', 'AllocType'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

        # region step 6: Approve block and allocate block and check 35= AK message
        # part 1: Approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        # end_of_part

        # part 2: Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        sec_acc_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            JavaApiFields.AllocAccountID.value: sec_acc_1,
            JavaApiFields.AllocQty.value: self.qty,
            JavaApiFields.BackOfficeNotes.value: back_office_notes,
            JavaApiFields.CDOrdFreeNotes.value: cd_ord_free_notes,
            JavaApiFields.AvgPx.value: self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        # end_of_part

        # part 3: Check 35 = AK message
        list_of_ignored_fields.extend(['ConfirmID', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmTransType', 'ConfirmType', 'ExecType', 'OrdStatus',
                                       'AllocType', 'tag11245'])

        change_parameters['AllocAccount'] = sec_acc_1
        change_parameters['AllocQty'] = self.qty
        change_parameters[JavaApiFields.BackOfficeNotes.value] = back_office_notes
        change_parameters['Text'] = cd_ord_free_notes
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                         ['AllocAccount', 'NoOrders'],
                                                         ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion
