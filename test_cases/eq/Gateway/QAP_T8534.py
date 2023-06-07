import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T8534(TestCase):
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
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.qty = '300'
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: create DMA  order
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.client_venue, self.mic, float(self.price))
            self.submit_request.set_default_dma_limit()
            self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.OrdQty.value: self.qty,
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.Price.value: self.price
            })
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            order_id = ord_reply[JavaApiFields.OrdID.value]
            cl_ord_id = ord_reply[JavaApiFields.ClOrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                ord_reply,
                'Verifying that DMA order created (precondition)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 1: Partially Fill DMA order
        contra_firm_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_contra_firm')
        execution_firm_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_executing_firm')
        counterpart_list = [contra_firm_for_es,
                            execution_firm_for_es]
        self.execution_report.set_default_trade(order_id)
        half_qty = str(float(self.qty) / 2)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.LastTradedQty.value: half_qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.LastCapacity.value:
                                                                 ExecutionReportConst.LastCapacity_Agency_FULL_VALUE.value,
                                                             JavaApiFields.LeavesQty.value: half_qty,
                                                             JavaApiFields.CumQty.value: half_qty,
                                                             JavaApiFields.PartiesList.value: {
                                                                 JavaApiFields.PartiesBlock.value:
                                                                     counterpart_list},
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verifying that order partially filled (step 1)')
        # endregion

        # region step 2: Fill DMA order
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        contra_firm_counterpart2 = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm_2')
        contra_firm2_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_contra_firm')
        counterpart_list.remove(contra_firm_for_es)
        counterpart_list.append(contra_firm2_for_es)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.LeavesQty.value: '0.0',
                                                             JavaApiFields.VenueExecID.value: bca.client_orderid(9),
                                                             JavaApiFields.PartiesList.value: {
                                                                 JavaApiFields.PartiesBlock.value:
                                                                     counterpart_list}

                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verifying that order fully filled (step 2)')
        execution_report_calculated = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                             ExecutionReportConst.ExecType_CAL.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Agency.value},
            execution_report_calculated,
            f'Verifying that calculated execution has properly defined {JavaApiFields.LastCapacity.value} (step 2)')
        self._verify_that_counterpart_is_present(contra_firm_counterpart, execution_report_calculated,
                                                 VerificationMethod.NOT_CONTAINS)
        self._verify_that_counterpart_is_present(contra_firm_counterpart2, execution_report_calculated,
                                                 VerificationMethod.NOT_CONTAINS)
        self._verify_that_counterpart_is_present(executing_firm_counterpart, execution_report_calculated,
                                                 VerificationMethod.CONTAINS)

        # endregion

        # region step 3: Check 35=8 (39 = B message)
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counter_part_id_executing_firm'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('entering_firm'),
            self.data_set.get_counterpart_id_fix('counterpart_java_api_user')]
        parties = {
            'NoParty': list_of_counterparts
        }
        change_parameters = {
            'ClOrdID': cl_ord_id,
            "NoParty": parties,
            'LastCapacity': '1'
        }
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy',
                                  'SettlCurrency', 'SecondaryOrderID', 'SecondaryExecID'
                                  ]
        execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        execution_report.change_parameters({'ExecType': 'B', "OrdStatus": "B"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def _verify_that_counterpart_is_present(self, counterpart, report, verification_method):
        word = 'present' if verification_method is VerificationMethod.CONTAINS else 'not present'
        self.java_api_manager.compare_values(
            {JavaApiFields.CounterpartID.value: counterpart[JavaApiFields.CounterpartID.value]},
            {JavaApiFields.CounterpartID.value: str(report)},
            f'Verify that Counterpart {counterpart[JavaApiFields.CounterpartID.value]} is {word} (step 3)',
            verification_method)
