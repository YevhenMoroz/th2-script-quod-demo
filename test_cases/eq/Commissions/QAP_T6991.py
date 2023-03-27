import logging
import time
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
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
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


class QAP_T6991(TestCase):
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
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
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

        # region create DMA  and fill it step 1
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region Partially trade DMA order (step 1)
        self.execution_report.set_default_trade(order_id)
        half_qty = int(int(self.qty) / 2)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": half_qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": half_qty,
                                                             "CumQty": half_qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Partially filled)', responses)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, actually_result,
            'Compare actually and expected result from step 1')
        # endregion

        # region step 3
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "LeavesQty": '0',
            "VenueExecID": bca.client_orderid(9),
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)

        print_message('Trade DMA  order (Fully Filled)', responses)
        actually_result = dict()
        actually_result.update({JavaApiFields.TransExecStatus.value: self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.TransExecStatus.value]})
        actually_result.update({JavaApiFields.PostTradeStatus.value: self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.PostTradeStatus.value]})

        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value}, actually_result,
            'Compare actually and expected result Execution from step 2')

        # verify that allocation report doesn`t have Total Fee
        fee_is_absent = not JavaApiFields.MiscFeesList.value in self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.AllocationReport.value}')
        # endregion

        # verify that confirmation report doesn`t have Total Fee
        fee_is_absent = not JavaApiFields.MiscFeesList.value in self.java_api_manager.get_last_message(
            ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.ConfirmationReport.value}')
        # endregion

        # comparing statuses of Allocation Report (step 2)
        allocation_message = self.java_api_manager.get_last_message(
            ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        actually_result.clear()
        actually_result.update({JavaApiFields.AllocStatus.value: allocation_message[JavaApiFields.AllocStatus.value]})
        actually_result.update({JavaApiFields.MatchStatus.value: allocation_message[JavaApiFields.MatchStatus.value]})
        actually_result.update(
            {JavaApiFields.AllocSummaryStatus.value: allocation_message[JavaApiFields.AllocSummaryStatus.value]})

        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            actually_result,
            'Compare actually and expected results  from step 2 for Allocation Report')

        # endregion

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
            'Compare actually and expected results  from step 2 for Confirmation')

        # region check 35=8 message step 4
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty', 'TransactTime', 'GrossTradeAmt',
                                  'ExDestination',
                                  'Side', 'AvgPx', 'SettlCurrency', 'SettlDate', 'TimeInForce',
                                  'PositionEffect', 'HandlInst', 'LeavesQty', 'CumQty',
                                  'LastPx', 'OrdType', 'SecondaryOrderID', 'OrderCapacity', 'QtyType',
                                  'Price', 'Instrument', 'BookID', 'QuodTradeQualifier', 'NoParty', 'ExDestination',
                                  'tag11245', 'GatingRuleName', 'GatingRuleCondName']
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.change_parameters({
            'ClOrdID': cl_ord_id,
            'OrderID': order_id,
            "ExecType": "B",
            "OrdStatus": "B"
        })
        misc_fee_rate = 5
        amount_of_fees = misc_fee_rate / 100 * int(self.qty) * int(self.price) / 100
        execution_report.change_parameters({'Currency': self.currency, 'CommissionData': '*',
                                            'tag5120': '*', 'ExecBroker': '*',
                                            'NoMiscFees': [{
                                                'MiscFeeAmt': amount_of_fees,
                                                'MiscFeeCurr': self.currency_post_trade,
                                                'MiscFeeType': '12'
                                            }]})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion
        #
        # region step 5
        new_avg_px = float(self.price) / 100
        list_of_ignored_fields.extend(['RootSettlCurrFxRateCalc', 'AllocID', 'NetMoney', 'TradeDate',
                                       'BookingType', 'RootSettlCurrency', 'AllocInstructionMiscBlock1',
                                       'Quantity', 'AllocTransType', 'RootSettlCurrFxRate', 'RootSettlCurrAmt',
                                       'GrossTradeAmt', 'AllocSettlCurrAmt', 'AllocSettlCurrency',
                                       'SettlCurrAmt', 'SettlCurrFxRate', 'SettlCurrFxRateCalc', 'ReportedPx',
                                       'OrderAvgPx'])
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.change_parameters({'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': order_id}],
                                             'AllocType': '2'})
        allocation_report.change_parameters({'AvgPx': new_avg_px, 'Currency': self.currency_post_trade,
                                             'tag5120': "*",
                                             'NoAllocs': [{'AllocAccount': self.alloc_account,
                                                           'AllocQty': self.qty,
                                                           'IndividualAllocID': '*',
                                                           'AllocNetPrice': '*',
                                                           'AllocPrice': '*',
                                                           'AllocInstructionMiscBlock2': '*'
                                                           }]
                                             })
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        allocation_report.change_parameters({'NoMiscFees': '#',
                                             'AllocType': '2'})
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
