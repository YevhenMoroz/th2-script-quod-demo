import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10963(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client_by_name("client_1")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.execution_report = ExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create DMA order via Fix
        self.fix_message.change_parameters({'Account': self.client})
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        execution_report = self.fix_manager.get_first_message('ExecutionReport').get_parameters()
        order_id = execution_report['OrderID']
        cl_ord_id = execution_report['ClOrdID']
        self.fix_manager.compare_values({'ExecType': 'A'}, execution_report,
                                        'Verify that order created and has Sts = Send (step 1)')
        # endregion

        # region step 2: Send 35 = 8 (39 = 0) message via BuyGateWay
        self.execution_report.set_default_new(order_id)
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verifying that order has Sts = Open')
        # endregion

        # region step 3: Execute CO order with ContraFirm
        contra_firm_java_api = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        contra_firm_party_role_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_contra_firm')
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.VenueExecID.value: bca.client_orderid(9),
                                                             JavaApiFields.LastTradedQty.value: self.qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.PartiesList.value: {
                                                                 JavaApiFields.PartiesBlock.value:
                                                                     [contra_firm_party_role_for_es]},
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                         })
        list_ignored_field = ['GatingRuleCondName', 'GatingRuleName', 'Parties',
                              'QuodTradeQualifier', 'BookID', 'SettlCurrency',
                              'TradeReportingIndicator', 'tag5120', 'LastMkt',
                              'ExecBroker']
        parties = {
            'NoParty': [
                self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
                self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4')
            ]
        }
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verify that order filled')
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix.set_default_filled(self.fix_message)
        execution_report_fix.change_parameters({"NoParty": parties})
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ignored_fields=list_ignored_field)
        # endregion

        # region step 4 : Cancel execution
        venue_exec_id = self.execution_report.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.VenueExecID.value]
        last_venue_order_id = self.execution_report.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.LastVenueOrdID.value]
        self.execution_report.set_default_cancel(venue_exec_id, last_venue_order_id, execution_report)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {JavaApiFields.PartiesList.value: {
                                                             JavaApiFields.PartiesBlock.value:
                                                                 [contra_firm_party_role_for_es]}})
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        print(execution_report)

        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
            execution_report, 'Verify that execution has ExecStatus = TradeCancel} (step 4)')
        result = contra_firm_java_api in execution_report[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        self.java_api_manager.compare_values({'ConterpartIsPresent': True},
                                             {'ConterpartIsPresent': result},
                                             'Verify that Conterpart is Present (step 4)')
        # endregion

        # region step 5: Check 35 =8 (150 = H) at BO gateway
        execution_report_fix.set_default_trade_cancel(self.fix_message)
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report_fix, ignored_fields=list_ignored_field)
        # endregion
