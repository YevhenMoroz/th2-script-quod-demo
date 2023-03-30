import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
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


class QAP_T8705(TestCase):
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
        # region step 1: create DMA  order
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.client_venue, self.mic, float(self.price))
            self.submit_request.get_parameters().clear()
            self.submit_request.set_default_dma_limit()
            self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price
            })
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            order_id = ord_reply[JavaApiFields.OrdID.value]
            cl_ord_id = ord_reply[JavaApiFields.ClOrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                ord_reply,
                'Verifying that DMA order created (step 1)')
        finally:
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 2: Fully Fill CO order
        contra_firm_party_role_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_contra_firm')
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
                                                             JavaApiFields.PartiesList.value: {
                                                                 JavaApiFields.PartiesBlock.value:
                                                                     [contra_firm_party_role_for_es]},
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        executing_firm_counterpart2 = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm2')
        counterparts_list = [executing_firm_counterpart, executing_firm_counterpart2, contra_firm_counterpart]
        self._verify_that_execution_has_properly_value(ExecutionReportConst.ExecType_TRD.value, counterparts_list)
        self._verify_that_execution_has_properly_value(ExecutionReportConst.ExecType_CAL.value, counterparts_list)
        # endregion

        # region step 3: Check 35=8 (39 = B, 39 = 2 messages)
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
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
            'LastCapacity': '#'
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
        execution_report.change_parameters({'ExecType': 'F', "OrdStatus": "2"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        execution_report.change_parameters({'ExecType': 'B', "OrdStatus": "B"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def _verify_that_execution_has_properly_value(self, exec_type, conterparts_list):
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  exec_type).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        counter_part_list = execution_report[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        execution_firm_is_absent = execution_firm2_is_absent = contra_firm_present = last_capacity_is_absent = False
        if conterparts_list[0] not in counter_part_list:
            execution_firm_is_absent = True
        if conterparts_list[1] not in counter_part_list:
            execution_firm2_is_absent = True
        if conterparts_list[2] in counter_part_list:
            contra_firm_present = True
        if JavaApiFields.LastCapacity.value not in str(execution_report):
            last_capacity_is_absent = True
        self.java_api_manager.compare_values({'ExecutionFirmIsAbsent': True,
                                              'ExecuitonFirm2IsAbsent': True,
                                              'ContraFirmIsPresent': True,
                                              'LastCapacityIsAbsent': True},
                                             {'ExecutionFirmIsAbsent': execution_firm_is_absent,
                                              'ExecuitonFirm2IsAbsent': execution_firm2_is_absent,
                                              'ContraFirmIsPresent': contra_firm_present,
                                              'LastCapacityIsAbsent': last_capacity_is_absent},
                                             f'Verifying that  Execution report({exec_type}) has counterparts (step 2)')
