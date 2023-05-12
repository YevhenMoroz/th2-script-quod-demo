import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7501(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.unallocate_request = BlockUnallocateRequest()
        self.qty = '300'
        self.result = None
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7501
        # region create CO  order (precondition)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price}
                                                       )

        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_ord_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        status = self.result.get_parameter('OrdReplyBlock')['TransStatus']
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            f'Comparing {OrderBookColumns.sts.value}')

        # endregion

        # region step 1 and step 2( trade CO order)
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        class_name.print_message('TRADE', responses)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        actually_result = self.result.get_parameters()['ExecutionReportBlock']['TransExecStatus']
        self.java_api_manager.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: actually_result},
            f'Comparing {OrderBookColumns.exec_sts.value}')

        # endregion

        # region complete CO order (step 3)
        responses = self.java_api_manager.send_message_and_receive_response(
            self.complete_order.set_default_complete(order_id))
        class_name.print_message('COMPLETE', responses)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        actually_post_trade_status = self.result.get_parameter('OrdReplyBlock')['PostTradeStatus']
        actually_done_for_day = self.result.get_parameter('OrdReplyBlock')['DoneForDay']
        self.java_api_manager.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_RDY.value,
             OrderBookColumns.done_for_day.value: OrderReplyConst.DoneForDay_YES.value},
            {OrderBookColumns.post_trade_status.value: actually_post_trade_status,
             OrderBookColumns.done_for_day.value: actually_done_for_day},
            "Comparing values of step 3")
        # endregion

        # region book CO order step 4 , 5
        settl_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': settl_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message('BOOK', responses)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message('APPROVE', responses)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        expected_alloc_status = self.result.get_parameters()['AllocationReportBlock']['AllocStatus']
        expected_match_status = self.result.get_parameters()['AllocationReportBlock']['MatchStatus']
        self.java_api_manager.compare_values({MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                                        MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value},
                                       {MiddleOfficeColumns.sts.value: expected_alloc_status,
                                        MiddleOfficeColumns.match_status.value: expected_match_status},
                                       'Comparing actual and expected result from step 5')
        # endregion

        # region allocate block (step 6, 7)
        alloc_qty = str(int((int(self.qty) / 2)))
        self.confirmation_request.set_default_allocation(alloc_id)
        sec_acc_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        sec_acc_2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        list_of_security_account = [sec_acc_1, sec_acc_2]
        for account in list_of_security_account:
            self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
                "AllocAccountID": account,
                'AllocQty': alloc_qty,
                'AvgPx': self.price,
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            class_name.print_message(f'CONFIRMATION FOR {account}', responses)
            self.return_result_for_confirmation_message_via_account(responses, account)
            expected_result = {AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                               AllocationsColumns.match_status.value: ConfirmationReportConst.MatchStatus_MAT.value}
            self.check_confirmation_message(expected_result,
                                            f'Comparing actual and expected result from step 7 for allocation {account}')

        expected_result = {MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                           MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
                           MiddleOfficeColumns.summary_status.value: AllocationReportConst.AllocSummaryStatus_MAG.value}
        message = f'Comparing actual and expected result from step 7 for middle office'
        self.check_allocation_message(responses, expected_result, message)

        # endregion

        # region unallocate order step 8
        self.unallocate_request.set_default(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.unallocate_request)
        class_name.print_message('UN_ALLOCATE', responses)
        for account in list_of_security_account:
            self.return_result_for_confirmation_message_via_account(responses, account)
            expected_result = {AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_CXL.value,
                               AllocationsColumns.match_status.value: ConfirmationReportConst.MatchStatus_UNM.value}
            self.check_confirmation_message(expected_result,
                                            f'Comparing actual and expected result from step 8 for allocation {account}')

        expected_result = {MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                           MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
                           MiddleOfficeColumns.summary_status.value: ''}
        message = f'Comparing actual and expected result from step 8 for middle office'
        self.check_allocation_message(responses, expected_result, message)
        # endregion

        # region step 9
        self.confirmation_request.set_default_allocation(alloc_id)
        sec_acc_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        sec_acc_2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        list_of_security_account = [sec_acc_1, sec_acc_2]
        for account in list_of_security_account:
            self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
                "AllocAccountID": account,
                'AllocQty': str(int((int(self.qty) / 2))),
                'AvgPx': self.price,
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            class_name.print_message(f'CONFIRMATION FOR {account}', responses)
            self.return_result_for_confirmation_message_via_account(responses, account)
            expected_result = {AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                               AllocationsColumns.match_status.value: ConfirmationReportConst.MatchStatus_MAT.value}
            self.check_confirmation_message(expected_result,
                                            f'Comparing actual and expected result from step 9 for allocation {account}')

        expected_result = {MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                           MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
                           MiddleOfficeColumns.summary_status.value: AllocationReportConst.AllocSummaryStatus_MAG.value}
        message = f'Comparing actual and expected result from step 9 for middle office'
        self.check_allocation_message(responses, expected_result, message)
        # endregion

        # region step 10 (check 35= AK messages)
        change_parameters = {
            'NoOrders': [{
                'ClOrdID': cl_ord_id,
                'OrderID': '*',
                'OrderAvgPx': '*'
            }]
        }
        list_of_ignored_fields = ['NoParty', 'Quantity', 'tag5120', 'TransactTime','tag11245',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney', 'Instrument',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'AllocInstructionMiscBlock2', 'ExecAllocGrp']

        list_of_ignored_fields.extend(['ConfirmID', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmTransType', 'ConfirmType'])

        for account in list_of_security_account:
            change_parameters['AllocAccount'] = account
            change_parameters['AllocQty'] = alloc_qty
            confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
            self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                             ['AllocAccount', 'NoOrders'],
                                                             ignored_fields=list_of_ignored_fields)
        # endregion

        # region check 35=J message (step 11)
        no_alloc_list = []
        list_of_ignored_fields.extend(['IndividualAllocID', 'AllocNetPrice', 'AllocPrice'])
        del change_parameters['AllocQty']
        del change_parameters['AllocAccount']
        for account in list_of_security_account:
            no_alloc_list.append({
                'AllocAccount': account,
                'AllocQty': alloc_qty,
            })
        change_parameters['AllocType'] = 2
        change_parameters['NoAllocs'] = no_alloc_list
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report,
                                                         key_parameters=['ClOrdID', 'AllocType', 'NoAllocs'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    def return_result_for_confirmation_message_via_account(self, responses, alloc_account):
        for response in responses:
            if 'ConfirmationReportBlock' in response.get_parameters():
                if 'AllocAccountID' in response.get_parameters()['ConfirmationReportBlock']:
                    if response.get_message_type() == ORSMessageType.ConfirmationReport.value and \
                            response.get_parameters()['ConfirmationReportBlock']['AllocAccountID'] == alloc_account:
                        self.result = response

    def check_confirmation_message(self, expected_result, message):
        actuall_allocation_status = self.result.get_parameter('ConfirmationReportBlock')['ConfirmStatus']
        actuall_allocation_match_status = self.result.get_parameter('ConfirmationReportBlock')['MatchStatus']
        self.java_api_manager.compare_values(
            expected_result,
            {AllocationsColumns.sts.value: actuall_allocation_status,
             AllocationsColumns.match_status.value: actuall_allocation_match_status},
            message)

    def check_allocation_message(self, responses, expected_result, message):
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        expected_alloc_status = self.result.get_parameters()['AllocationReportBlock']['AllocStatus']
        expected_match_status = self.result.get_parameters()['AllocationReportBlock']['MatchStatus']
        if 'AllocSummaryStatus' in self.result.get_parameters()['AllocationReportBlock']:
            expected_summary_status = self.result.get_parameters()['AllocationReportBlock']['AllocSummaryStatus']
        else:
            expected_summary_status = ''
        self.java_api_manager.compare_values(expected_result,
                                       {MiddleOfficeColumns.sts.value: expected_alloc_status,
                                        MiddleOfficeColumns.match_status.value: expected_match_status,
                                        MiddleOfficeColumns.summary_status.value: expected_summary_status},
                                       message)

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
