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
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, ConfirmationReportConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7503(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
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
        self.order_book.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            f'Comparing {OrderBookColumns.sts.value}')

        # endregion

        # region step 1 and step 2( trade CO order)
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        actually_result = self.result.get_parameters()['ExecutionReportBlock']['TransExecStatus']
        self.return_result(responses, ORSMessageType.OrdNotification.value)
        self.order_book.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: actually_result, },
            f'Comparing {OrderBookColumns.exec_sts.value}')
        # endregion

        # region complete CO order (step 3)
        responses = self.java_api_manager.send_message_and_receive_response(
            self.complete_order.set_default_complete(order_id))
        self.return_result(responses, ORSMessageType.OrdReply.value)
        actually_post_trade_status = self.result.get_parameter('OrdReplyBlock')['PostTradeStatus']
        actually_done_for_day = self.result.get_parameter('OrdReplyBlock')['DoneForDay']
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_RDY.value,
             OrderBookColumns.done_for_day.value: OrderReplyConst.DoneForDay_YES.value},
            {OrderBookColumns.post_trade_status.value: actually_post_trade_status,
             OrderBookColumns.done_for_day.value: actually_done_for_day},
            "Comparing values of step 3")
        # endregion

        # region book and approve CO order step 4 , 5 and 6
        gross_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   "AllocInstructionMiscBlock": {
                                                                       "AllocInstructionMisc0": "BOF1C",
                                                                       "AllocInstructionMisc1": "BOF2C",
                                                                       "AllocInstructionMisc2": "BOF3C",
                                                                       "AllocInstructionMisc3": "BOF4C",
                                                                       "AllocInstructionMisc4": "BOF5C"
                                                                   }
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        self.return_result(responses, ORSMessageType.OrdUpdate.value)
        actually_post_trade_status = self.result.get_parameter('OrdUpdateBlock')['PostTradeStatus']
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {OrderBookColumns.post_trade_status.value: actually_post_trade_status},
            'Comparing actual and expected result from step 4, 5')
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        expected_alloc_status = self.result.get_parameters()['AllocationReportBlock']['AllocStatus']
        expected_match_status = self.result.get_parameters()['AllocationReportBlock']['MatchStatus']
        self.order_book.compare_values({MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                                        MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value},
                                       {MiddleOfficeColumns.sts.value: expected_alloc_status,
                                        MiddleOfficeColumns.match_status.value: expected_match_status},
                                       'Comparing actual and expected result from step 6')
        # endregion

        # region allocate block (step 7 and 8)
        self.confirmation_request.set_default_allocation(alloc_id)
        sec_acc_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        sec_acc_2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        list_of_security_account = [sec_acc_1, sec_acc_2]
        for account in list_of_security_account:
            self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
                "AllocAccountID": account,
                'AllocQty': str(int((int(self.qty) / 2))),
                'AvgPx': self.price,
                'ConfirmationMiscBlock': {'ConfirmationMisc0': f"BOF1A{list_of_security_account.index(account)}",
                                          'ConfirmationMisc1': f"BOF2A{list_of_security_account.index(account)}",
                                          'ConfirmationMisc2': f"BOF3A{list_of_security_account.index(account)}",
                                          'ConfirmationMisc3': f"BOF4A{list_of_security_account.index(account)}",
                                          'ConfirmationMisc4': f"BOF5A{list_of_security_account.index(account)}"}
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            self.return_result(responses, ORSMessageType.ConfirmationReport.value)
            actuall_allocation_status = self.result.get_parameter('ConfirmationReportBlock')['ConfirmStatus']
            actuall_allocation_match_status = self.result.get_parameter('ConfirmationReportBlock')['MatchStatus']

            self.order_book.compare_values(
                {AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                 AllocationsColumns.match_status.value: ConfirmationReportConst.MatchStatus_MAT.value},
                {AllocationsColumns.sts.value: actuall_allocation_status,
                 AllocationsColumns.match_status.value: actuall_allocation_match_status},
                f'Comparing actual and expected result from step 8 for allocation {account}')

        self.return_result(responses, ORSMessageType.AllocationReport.value)
        expected_alloc_status = self.result.get_parameters()['AllocationReportBlock']['AllocStatus']
        expected_match_status = self.result.get_parameters()['AllocationReportBlock']['MatchStatus']
        expected_summary_status = self.result.get_parameters()['AllocationReportBlock']['AllocSummaryStatus']
        self.order_book.compare_values({MiddleOfficeColumns.sts.value: AllocationReportConst.AllocStatus_ACK.value,
                                        MiddleOfficeColumns.match_status.value: AllocationReportConst.MatchStatus_MAT.value,
                                        MiddleOfficeColumns.summary_status.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
                                       {MiddleOfficeColumns.sts.value: expected_alloc_status,
                                        MiddleOfficeColumns.match_status.value: expected_match_status,
                                        MiddleOfficeColumns.summary_status.value: expected_summary_status},
                                       f'Comparing actual and expected result from step 8 for middle office')

        # endregion

        # region check message 35=J step 9
        change_parameters = {
            'AllocType': 5,
            'NoOrders': [{
                'ClOrdID': cl_ord_id,
                'OrderID': '*'
            }],
            "AllocInstructionMiscBlock1": {
                "BOMiscField0": "BOF1C",
                "BOMiscField1": "BOF2C",
                "BOMiscField2": "BOF3C",
                "BOMiscField3": "BOF4C",
                "BOMiscField4": "BOF5C"
            }
        }
        list_of_ignored_fields = ['NoParty', 'Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney', 'Instrument',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocQty', 'AllocPrice']
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # region check 35=J message step 10
        no_alloc_list = []
        dict_alloc_misc_fields = list()
        for account in list_of_security_account:
            dict_alloc_misc_fields.append({
                'BOMiscField5': f"BOF1A{list_of_security_account.index(account)}",
                'BOMiscField6': f"BOF2A{list_of_security_account.index(account)}",
                'BOMiscField7': f"BOF3A{list_of_security_account.index(account)}",
                'BOMiscField8': f"BOF4A{list_of_security_account.index(account)}",
                'BOMiscField9': f"BOF5A{list_of_security_account.index(account)}"
            })
            no_alloc_list.append({
                'AllocAccount': account,
                'AllocInstructionMiscBlock2': dict_alloc_misc_fields[list_of_security_account.index(account)]
            })
        change_parameters['AllocType'] = 2
        change_parameters['NoAllocs'] = no_alloc_list
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # region check 35 = AK messages step 11
        list_of_ignored_fields.extend(['ConfirmID', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmTransType', 'ConfirmType'])
        del change_parameters['NoAllocs']
        del change_parameters['AllocType']
        for account in list_of_security_account:
            change_parameters['AllocAccount'] = account
            change_parameters.update(
                {'AllocInstructionMiscBlock2': dict_alloc_misc_fields[list_of_security_account.index(account)]})
            confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
            self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                             ['AllocAccount', 'NoOrders'],
                                                             ignored_fields=list_of_ignored_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
