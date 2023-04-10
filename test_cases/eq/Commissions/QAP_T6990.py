import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst, ConfirmationReportConst, AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6990(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '6990'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_pt_10')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_10_acc_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_fees()
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create CO  precondition
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create CO order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region partially trade CO order (step 1)
        half_qty = int(int(self.qty) / 2)
        self.trade_entry.set_default_trade(order_id, self.price, half_qty)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.venue_mic})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        print_message('Trade CO  order (Partially filled)', responses)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, actually_result,
            'Compare actually and expected result from step 1')
        # endregion

        # region step 2
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        print_message('Trade CO  order (Fully Filled)', responses)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, actually_result,
            'Compare actually and expected result from step 2')
        # endregion

        # region complete CO order (step 3)
        self.complete_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        print_message("Complete CO order", responses)
        actually_result = dict()
        actually_result.update({JavaApiFields.PostTradeStatus.value: self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.PostTradeStatus.value]})
        allocation_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        actually_result.update({JavaApiFields.AllocStatus.value: allocation_message[JavaApiFields.AllocStatus.value]})
        actually_result.update({JavaApiFields.MatchStatus.value: allocation_message[JavaApiFields.MatchStatus.value]})
        actually_result.update(
            {JavaApiFields.AllocSummaryStatus.value: allocation_message[JavaApiFields.AllocSummaryStatus.value]})

        # comparing statuses of allocation report  and order reply
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            actually_result,
            'Compare actually and expected results  from step 3 for Allocation Report')

        # comparing statuses of confirmation report
        actually_result.clear()
        confirmation_message = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        actually_result.update(
            {JavaApiFields.ConfirmStatus.value: confirmation_message[JavaApiFields.ConfirmStatus.value]})
        actually_result.update({JavaApiFields.MatchStatus.value: confirmation_message[JavaApiFields.MatchStatus.value]})

        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value}, actually_result,
            'Compare actually and expected results  from step 3 for Confirmation')

        # verify that allocation report doesn`t have Total Fee
        fee_is_absent = not JavaApiFields.MiscFeesList.value in self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.AllocationReport.value}')

        # verify that confirmation report doesn`t have Total Fee
        fee_is_absent = not JavaApiFields.MiscFeesList.value in self.java_api_manager.get_last_message(
                                                ORSMessageType.ConfirmationReport.value).get_parameters()[
                                                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.ConfirmationReport.value}')
        # endregion

        # region step 4
        misc_fee_rate = 5
        amount_of_fees = misc_fee_rate / 100 * int(self.qty) * int(self.price) / 100
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_CAL.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0]
        expected_result = {JavaApiFields.MiscFeeRate.value: str(float(misc_fee_rate)),
                           JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
                           JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
                           JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.MiscFeeAmt.value: str(amount_of_fees)}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Comparing expected and actually result from step 4')
        # endregion

        # region check 35=8 message step 5
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty', 'TransactTime', 'GrossTradeAmt',
                                  'ExDestination','ExecAllocGrp',
                                  'Side', 'AvgPx', 'SettlCurrency', 'SettlDate', 'TimeInForce',
                                  'PositionEffect', 'HandlInst', 'LeavesQty', 'CumQty',
                                  'LastPx', 'OrdType', 'SecondaryOrderID', 'OrderCapacity', 'QtyType',
                                  'Price', 'Instrument', 'BookID', 'QuodTradeQualifier', 'NoParty', 'ExDestination',
                                  'Side', 'OrderAvgPx', 'GatingRuleCondName', 'GatingRuleName']
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.change_parameters({
            'ClOrdID': cl_ord_id,
            'OrderID': order_id,
            "ExecType": "B",
            "OrdStatus": "B"
        })
        execution_report.change_parameters({'Currency': self.currency, 'CommissionData': '*',
                                            'tag5120': '*', 'ExecBroker': '*',
                                            'NoMiscFees': [{
                                                'MiscFeeAmt': amount_of_fees,
                                                'MiscFeeCurr': self.currency_post_trade,
                                                'MiscFeeType': '12'
                                            }]})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # region step 6
        new_avg_px = float(self.price) / 100
        list_of_ignored_fields.extend(['RootSettlCurrFxRateCalc', 'AllocID', 'NetMoney', 'TradeDate',
                                       'BookingType', 'RootSettlCurrency', 'AllocInstructionMiscBlock1',
                                       'Quantity', 'AllocTransType', 'RootSettlCurrFxRate', 'RootSettlCurrAmt',
                                       'GrossTradeAmt', 'AllocSettlCurrAmt', 'AllocSettlCurrency',
                                       'SettlCurrAmt', 'SettlCurrFxRate', 'SettlCurrFxRateCalc', 'ReportedPx',
                                       'tag11245'])
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.change_parameters({'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': order_id}],
                                             'AllocType': '5'})
        allocation_report.change_parameters({'AvgPx': new_avg_px, 'Currency': self.currency_post_trade,
                                             'tag5120': "*",
                                             })
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        allocation_report.change_parameters({'NoMiscFees': '#',
                                             'AllocType': '2',
                                             'NoAllocs': [{'AllocAccount': self.alloc_account,
                                                           'AllocQty': self.qty,
                                                           'IndividualAllocID': '*',
                                                           'AllocNetPrice': '*',
                                                           'AllocPrice': '*',
                                                           'AllocInstructionMiscBlock2': '*'
                                                           }]
                                             })
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        list_of_ignored_fields.extend(['ConfirmType', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmID', 'ConfirmTransType'])
        confirmation_report.change_parameters({'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': order_id
        }]})
        confirmation_report.change_parameters(
            {'AvgPx': new_avg_px, 'Currency': self.currency_post_trade,
             'tag5120': '*', 'AllocInstructionMiscBlock2': '*'})
        confirmation_report.change_parameters({'AllocQty': self.qty,
                                               'AllocAccount': self.alloc_account,
                                               'NoMiscFees': '#'})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report, ['ClOrdID', 'AllocAccount'],
                                                         ignored_fields=list_of_ignored_fields)
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
