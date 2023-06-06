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
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


def _verify_that_counterpart_present(expected_counterparts, actually_counterparts):
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


class QAP_T8527(TestCase):
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
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO  order (precondition)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # endregion

        # region step 1:  Partially fill CO order
        contra_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        executing_firm_counterpart = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm')
        counterpart_list_and_capacity = {JavaApiFields.CounterpartList.value: {
            JavaApiFields.CounterpartBlock.value: [
                contra_firm_counterpart,
                executing_firm_counterpart,
            ]},
            JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Principal.value}
        qty = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        price = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        half_qty = str(float(qty) / 2)

        self.trade_entry_message.set_default_trade(order_id, price, half_qty)
        self.trade_entry_message.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                            counterpart_list_and_capacity)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)

        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        value = _verify_that_counterpart_present(
            counterpart_list_and_capacity[JavaApiFields.CounterpartList.value][
                JavaApiFields.CounterpartBlock.value],
            execution_report[
                JavaApiFields.CounterpartList.value][
                JavaApiFields.CounterpartBlock.value])
        self.java_api_manager.compare_values({'CounterpartsArePresent': True},
                                             {'CounterpartsArePresent': value},
                                             'Verifying first Execution report has counterparts (step 1)')
        self.java_api_manager.compare_values(
            {JavaApiFields.LastCapacity.value: counterpart_list_and_capacity[JavaApiFields.LastCapacity.value],
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report,
            f'Verify that order is partially filled and has correct {JavaApiFields.LastCapacity.value} (step 1)')
        # endregion

        # region step 2: fully fill CO order
        exec_firm_ctrpt_second = self.data_set.get_counterpart_id_java_api('counterpart_executing_firm2')
        counterpart_list_and_capacity.update({JavaApiFields.CounterpartList.value: {
            JavaApiFields.CounterpartBlock.value: [
                contra_firm_counterpart,
                exec_firm_ctrpt_second,
            ]},
            JavaApiFields.LastCapacity.value: ExecutionReportConst.LastCapacity_Agency.value})
        self.trade_entry_message.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                            counterpart_list_and_capacity)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        value = _verify_that_counterpart_present(
            counterpart_list_and_capacity[JavaApiFields.CounterpartList.value][
                JavaApiFields.CounterpartBlock.value],
            execution_report[
                JavaApiFields.CounterpartList.value][
                JavaApiFields.CounterpartBlock.value])
        self.java_api_manager.compare_values({'CounterpartsArePresent': True},
                                             {'CounterpartsArePresent': value},
                                             'Verifying first Execution report has counterparts (step 2)')
        self.java_api_manager.compare_values(
            {JavaApiFields.LastCapacity.value: counterpart_list_and_capacity[JavaApiFields.LastCapacity.value],
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            f'Verify that order is partially filled and has correct {JavaApiFields.LastCapacity.value} (step 2)')
        # endregion

        # region step 3: Complete CO order
        self.java_api_manager.send_message_and_receive_response(self.complete_order.set_default_complete(order_id))
        calculated_execution = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        contra_firm_is_present = contra_firm_counterpart in calculated_execution[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        executing_firm_counterpart_is_present = not executing_firm_counterpart in \
                                                    calculated_execution[JavaApiFields.CounterpartList.value][
                                                        JavaApiFields.CounterpartBlock.value]
        executing_firm_counterpart2_is_present = not exec_firm_ctrpt_second in \
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
                                             'Verify that only ContraFirm counterpart present (step 3)')
        # endregion

        # region step 3: Check 35=8 (39 = B message)
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
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
                                  'AllocID', 'Currency', 'NetMoney', 'SettlCurrency', 'NoPartySubIDs',
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
