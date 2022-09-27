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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.java_api_constants import ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, AllocationInstructionConst, ConfirmationReportConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7500(TestCase):
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
        self.qty = '100'
        self.result = None
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO  order (precondition)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                                               'OrdQty': self.qty,
                                                                               'AccountGroupID': self.client}
                                                       )
        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        self.return_result(responses, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_ord_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        # endregion

        # region step 1 and step 2( trade CO order)
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        actually_result = self.result.get_parameters()['ExecutionReportBlock']['TransExecStatus']
        self.order_book.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: actually_result},
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

        # region book CO order step 4 , 5
        self.price = str(int(self.price) * 2)
        settl_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.set_default_book(order_id)
        new_currrency = self.data_set.get_currency_by_name('currency_5')
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'Currency': new_currrency,
                                                                   'SettlCurrFxRate': '2',
                                                                   'SettlCurrFxRateCalc': 'M',
                                                                   'SettlCurrAmt': settl_currency_amt,
                                                                   'SettlCurrency': new_currrency,
                                                                   'RecomputeInSettlCurrency': 'Y',
                                                                   'ComputeFeesCommissions': 'N',
                                                                   'GrossTradeAmt': settl_currency_amt,
                                                                   'SettlType': AllocationInstructionConst.SettlType_REG.value,
                                                                   'AvgPx': self.price
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.return_result(responses, ORSMessageType.OrdUpdate.value)
        actually_post_trade_status = self.result.get_parameter('OrdUpdateBlock')['PostTradeStatus']
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value},
                                       {OrderBookColumns.post_trade_status.value: actually_post_trade_status},
                                       'Comparing actual and expected result from step 4, 5')
        # endregion

        # region approve order step 6
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

        # region allocate block (step 7, 8)
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
            self.return_result(responses, ORSMessageType.ConfirmationReport.value)
            actuall_allocation_status = self.result.get_parameter('ConfirmationReportBlock')['ConfirmStatus']
            actuall_allocation_match_status = self.result.get_parameter('ConfirmationReportBlock')['MatchStatus']

            self.order_book.compare_values({AllocationsColumns.sts.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
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

        # region check 35=J message on fix BackOffice gateway (step 9)
        change_parameters = {
            'BookingType': '*',
            'RootSettlCurrency': new_currrency,
            'tag5120': '*',
            'AllocType': '*',
            'AllocTransType': '*',
            'SettlType': '*',
            'RootSettlCurrAmt': '*',
            'NoParty': '*',
            'AllocInstructionMiscBlock1': '*',
            'Quantity': self.qty,
            'TransactTime': '*',
            'ReportedPx': '*',
            'Side': '*',
            'AvgPx': self.price,
            'QuodTradeQualifier': '*',
            'BookID': '*',
            'NoOrders': [{
                'ClOrdID': cl_ord_id,
                'OrderID': '*'
            }],
            'SettlDate': '*',
            'AllocID': '*',
            'Currency': new_currrency,
            'NetMoney': '*',
            'Instrument': '*',
            'TradeDate': '*',
            'GrossTradeAmt': '*',
        }
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report)
        # endregion

        # region check allocation message 35=J 626 =2
        change_parameters['AllocType'] = '2'
        change_parameters['NoAllocs'] = [{
            'IndividualAllocID': '*',
            'AllocNetPrice': '*',
            'AllocQty': '*',
            'AllocSettlCurrency': new_currrency,
            'SettlCurrency': new_currrency,
            'AllocAccount': sec_acc_1,
            'AllocPrice': '*'
        },
            {'IndividualAllocID': '*',
             'AllocNetPrice': '*',
             'AllocQty': '*',
             'AllocSettlCurrency': new_currrency,
             'SettlCurrency': new_currrency,
             'AllocAccount': sec_acc_2,
             'AllocPrice': '*'
             }]
        allocation_report = FixMessageAllocationInstructionReportOMS(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report)
        # endregion

        # region step 10
        list_fields_for_delete = ['NoAllocs', 'BookingType', 'RootSettlCurrency', 'Quantity', 'AllocType',
                                  'AllocTransType', 'RootSettlCurrAmt']
        for field in list_fields_for_delete:
            del change_parameters[field]
        change_parameters.update({'AllocQty': '*', 'ConfirmType': '*', 'SettlCurrency': new_currrency,
                                  'MatchStatus': '*', 'ConfirmStatus': '*',
                                  'CpctyConfGrp': '*', 'ConfirmTransType': '0',
                                  'ConfirmID': '*'
                                  })
        change_parameters['AllocAccount'] = sec_acc_1
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set, change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                         ['AllocAccount', 'ConfirmTransType', 'NoOrders'])
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
