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
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, JavaApiFields, ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T8741(TestCase):
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
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.qty = '300'
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
        self.java_api_manager.send_message_and_receive_response(self.submit_request, response_time=20000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # endregion

        # region step 1: Partially Fill CO order
        half_qty = str(float(self.qty) / 2)
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        counterpart_list = {JavaApiFields.CounterpartList.value: {
            JavaApiFields.CounterpartBlock.value: [
                contra_firm_counterpart,
                executing_firm_counterpart,
            ]}}
        self.trade_entry_message.set_default_trade(order_id, self.price, half_qty)
        self.trade_entry_message.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                            {
                                                                JavaApiFields.CounterpartList.value:
                                                                    counterpart_list[
                                                                        JavaApiFields.CounterpartList.value],
                                                                JavaApiFields.LastCapacity.value:
                                                                    ExecutionReportConst.LastCapacity_Principal.value})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        value = self._verify_that_counterpart_present(counterpart_list[JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value],
                                                      execution_report[JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value])
        self.java_api_manager.compare_values({'CounterpartsArePresent': True},
                                             {'CounterpartsArePresent': value},
                                             'Verifying that  Execution report has counterparts (step 1)')
        self.java_api_manager.compare_values({JavaApiFields.ExecOrigin.value: ExecutionReportConst.ExecOrigin_M.value,
                                              JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Principal.value},
                                             execution_report,
                                             f'Verifying that Execution has properly {JavaApiFields.LastCapacity.value} and {JavaApiFields.ExecOrigin.value} (step 1)')
        # endregion

        # region step 2: Create Child DMA order
        cl_ord_id_child = bca.client_orderid(15)
        self.submit_request.get_parameters().clear()
        self.submit_request.set_default_child_dma(order_id, client_order_id=cl_ord_id_child)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
            "OrdQty": half_qty,
            "AccountGroupID": self.client,
            "Price": self.price
        })
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        child_ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                 ExecutionPolicyConst.DMA.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        child_order_id = child_ord_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             child_ord_reply,
                                             'Verifying that Child order created (step 2)')

        # endregion

        # region step 3 : Trade DMA order
        contra_firm_party_role_for_es = self.data_set.get_counterpart_java_api_for_es('counterpart_contra_firm')
        executing_firm_2_party_role_for_es = self.data_set.get_counterpart_java_api_for_es(
            'counterpart_executing_firm2')
        self.execution_report.set_default_trade(child_order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             JavaApiFields.Side.value: "Buy",
                                                             JavaApiFields.LastTradedQty.value: half_qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: "Limit",
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.ExecType.value: "Trade",
                                                             JavaApiFields.TimeInForce.value: "Day",
                                                             JavaApiFields.LeavesQty.value: '0',
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Agency_FULL_VALUE.value,
                                                             JavaApiFields.PartiesList.value: {
                                                                 JavaApiFields.PartiesBlock.value:
                                                                     [contra_firm_party_role_for_es,
                                                                      executing_firm_2_party_role_for_es]},
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: half_qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict={order_id: order_id})
        execution_report_parent_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        executing_firm_counterpart2 = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm2')
        counterpart_list[JavaApiFields.CounterpartList.value][JavaApiFields.CounterpartBlock.value][
            1] = executing_firm_counterpart2
        value = self._verify_that_counterpart_present(counterpart_list[JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value],
                                                      execution_report_parent_order[
                                                          JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value])
        self.java_api_manager.compare_values({'CounterpartsArePresent': True},
                                             {'CounterpartsArePresent': value},
                                             'Verifying that second Execution report has counterparts (step 3)')
        self.java_api_manager.compare_values({JavaApiFields.ExecOrigin.value: ExecutionReportConst.ExecOrigin_E.value,
                                              JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Agency.value},
                                             execution_report_parent_order,
                                             f'Verifying that Execution has properly {JavaApiFields.LastCapacity.value} and {JavaApiFields.ExecOrigin.value} (step 3)')
        # endregion

        # region step 4: Complete CO order
        self.java_api_manager.send_message_and_receive_response(self.complete_order.set_default_complete(order_id))
        calculated_execution = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        contra_firm_is_present = contra_firm_counterpart in calculated_execution[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        executing_firm_counterpart_is_present = not executing_firm_counterpart in \
                                                calculated_execution[JavaApiFields.CounterpartList.value][
                                                    JavaApiFields.CounterpartBlock.value]
        executing_firm_counterpart2_is_present = not executing_firm_counterpart2 in \
                                                 calculated_execution[JavaApiFields.CounterpartList.value][
                                                     JavaApiFields.CounterpartBlock.value]
        last_capacity_is_present = not JavaApiFields.LastCapacity.value in str(calculated_execution)
        self.java_api_manager.compare_values({'ContraFirmPresent': True,
                                              'ExecutionFirmIsAbsent': True,
                                              'ExecutionFirm2IsAbsent': True,
                                              'LastCapacityIsAbsent': True},
                                             {'ContraFirmPresent': contra_firm_is_present,
                                              'ExecutionFirmIsAbsent': executing_firm_counterpart_is_present,
                                              'ExecutionFirm2IsAbsent': executing_firm_counterpart2_is_present,
                                              'LastCapacityIsAbsent': last_capacity_is_present},
                                             'Verify that only ContraFirm counterpart present (step 4)'
                                             )
        # endregion

        # region step 5: Check 35=8 (39 = B message)
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
                                  'GatingRuleName', 'GatingRuleCondName'
                                  ]
        execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        execution_report.change_parameters({'ExecType': 'B', "OrdStatus": "B"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def _verify_that_counterpart_present(self, expected_counterparts, actually_counterparts):
        results = []
        results.extend(
            False
            for expected_counterpart in expected_counterparts
            if expected_counterpart not in actually_counterparts
        )
        if False in results:
            results.clear()
            return False
        else:
            results.clear()
            return True
