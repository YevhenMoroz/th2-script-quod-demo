import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T8703(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
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

        # region step 1: Fully Fill CO order
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        counterpart_list = {JavaApiFields.CounterpartList.value: {
            JavaApiFields.CounterpartBlock.value: [
                contra_firm_counterpart,
                executing_firm_counterpart,
            ]}}
        self.trade_entry_message.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry_message.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                            counterpart_list)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self._verify_that_counterpart_present(counterpart_list[JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value],
                                                      execution_report[JavaApiFields.CounterpartList.value][
                                                          JavaApiFields.CounterpartBlock.value], 'step 1')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            f'Verifying that Order fully filled (step 1)')
        # endregion

        # region step 2: Complete CO order
        self.java_api_manager.send_message_and_receive_response(self.complete_order.set_default_complete(order_id))
        calculated_execution = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]

        self._verify_that_counterpart_present(counterpart_list[JavaApiFields.CounterpartList.value][
                                                  JavaApiFields.CounterpartBlock.value],
                                              calculated_execution[JavaApiFields.CounterpartList.value][
                                                  JavaApiFields.CounterpartBlock.value], 'step 2')
        last_capacity_is_present = not JavaApiFields.LastCapacity.value in str(calculated_execution)
        self.java_api_manager.compare_values({'LastCapacityIsAbsent': True},
                                             {'LastCapacityIsAbsent': last_capacity_is_present},
                                             f'Verify that only {JavaApiFields.LastCapacity.value} is absent (step 2)')

        # endregion

        # region step 3: Check 35=8 (39 = B message)
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('entering_firm'),
            self.data_set.get_counterpart_id_fix('counter_part_id_executing_firm'),
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
        execution_report.change_parameters({'ExecType': 'F', "OrdStatus": "2"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        execution_report.change_parameters({'ExecType': 'B', "OrdStatus": "B"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def _verify_that_counterpart_present(self, expected_counterparts, actually_counterparts, step):
        results = []
        results.extend(
            False
            for expected_counterpart in expected_counterparts
            if expected_counterpart not in actually_counterparts
        )
        if False in results:
            results.clear()
            value = False
        else:
            results.clear()
            value = True
        self.java_api_manager.compare_values({'CounterpartsArePresent': True},
                                             {'CounterpartsArePresent': value},
                                             f'Verifying that  Execution report has counterparts ({step})')
