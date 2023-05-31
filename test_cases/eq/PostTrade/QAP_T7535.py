import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationInstructionConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7535(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.all_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.currency = self.data_set.get_currency_by_name('currency_5')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('Account', self.client)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.allocation_message = FixMessageAllocationInstructionReportOMS()
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create order and trade dma order (precondition)
        order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(10)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(nos_rule)
        #  endregion

        # region book order (step 1, step 2)
        rate = '2'
        new_avg_px = int(self.price) * int(rate)
        gross_trade_sett_curr_amt = str(int(self.price) * 2 * int(self.qty))
        self.allocation_instruction.set_default_book(order_id)
        settl_dict = {JavaApiFields.SettlCurrency.value: self.currency,
                      JavaApiFields.SettlCurrFxRate.value: str(float(rate)),
                      JavaApiFields.SettlCurrFxRateCalc.value: AllocationInstructionConst.SettlCurrFxRateCalc_M.value}
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "Qty": self.qty,
            "AvgPx": str(new_avg_px),
            "SettlCurrAmt": gross_trade_sett_curr_amt,
            'GrossTradeAmt': gross_trade_sett_curr_amt,
            "Currency": self.currency,
            "InstrID": self.instr_id,
            'RecomputeInSettlCurrency': 'Yes'
        })
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', settl_dict)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Book order", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values({
            JavaApiFields.AvgPrice.value: str(float(new_avg_px)),
            JavaApiFields.Currency.value: self.currency,
            JavaApiFields.NetMoney.value: str(float(gross_trade_sett_curr_amt))
        }, allocation_report, 'Checking that values re-computed')
        #  endregion

        # region check Alloc Report (step 3)
        list_of_ignored_fields = ['Account', 'RootSettlCurrFxRateCalc', 'RootSettlCurrFxRate',
                                  'OrderAvgPx', 'AllocInstructionMiscBlock2', 'SettlCurrFxRateCalc',
                                  'SettlCurrFxRate', 'tag11245', 'ExecAllocGrp']
        self.allocation_message.set_default_ready_to_book(self.fix_message)
        self.allocation_message.change_parameters(
            {'AvgPx': str(new_avg_px), 'Currency': self.currency, 'RootSettlCurrency': self.currency,
             "RootSettlCurrAmt": gross_trade_sett_curr_amt,
             'tag5120': "*", "GrossTradeAmt": gross_trade_sett_curr_amt,
             'NetMoney': gross_trade_sett_curr_amt})
        self.fix_verifier.check_fix_message_fix_standard(self.allocation_message, ignored_fields=list_of_ignored_fields)
        #  endregion

        # region approve and allocate
        self.approve_request.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_request)
        print_message("Approve block", responses)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.all_acc,
            "AllocQty": self.qty,
            "AvgPx": new_avg_px,
            "InstrID": self.instr_id})
        resp = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print(resp)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report,
            'Check expected and actually results from step 4 (concerning block)')
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value}, confirmation_report,
            'Check expected and actually results from step 4 (concerning allocation)')
        #  endregion

        # region check confirmation report (step 5)
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters(
            {'AvgPx': new_avg_px, 'Currency': self.currency, "tag5120": "*",
             "GrossTradeAmt": gross_trade_sett_curr_amt,
             "NetMoney": gross_trade_sett_curr_amt,
             "SettlCurrAmt": gross_trade_sett_curr_amt, "SettlCurrency": self.currency,
             "Account": self.client, "AllocInstructionMiscBlock2": '*'})
        self.fix_verifier.check_fix_message_fix_standard(conf_report, ignored_fields=list_of_ignored_fields)
        #  endregion
