import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, \
    ExecutionReportConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.PositionTransferCancelRequest import PositionTransferCancelRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6998(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ord_report_oms = OrdReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step precondition : Create CO order , create child CO order and create GrandChild DMA order
        # part 1: Create CO order
        self._set_fees()
        self.new_order_single.set_default_care_limit()
        self.new_order_single.change_parameters({'Account': self.client})
        qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        price = self.new_order_single.get_parameter('Price')
        self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = self.fix_manager.get_last_message("ExecutionReport").get_parameter("OrderID")
        # end_of_part

        # part 2: Create child CO order from CO order
        instrument = self.data_set.get_instrument_id_by_name('instrument_2')
        listing = self.data_set.get_listing_id_by_name('listing_3')
        self.order_submit.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                 self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 SubmitRequestConst.USER_ROLE_1.value, order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.OrdQty.value: qty,
            JavaApiFields.InstrID.value: instrument,
            'ListingList': {'ListingBlock': [{'ListingID': listing}]},
            JavaApiFields.Price.value: price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=18000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        child_care_order_id = order_reply[JavaApiFields.OrdID.value]
        # end_of_part
        # endregion

        # region precondition part 3 and step 1: Create child DMA order from Child CO order and send 35=8 message
        child_dma_order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.account,
                                                                                                  self.mic,
                                                                                                  float(price))
            self.order_submit.get_parameters().clear()
            self.order_submit.set_default_child_dma(child_care_order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.OrdQty.value: qty,
                JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                JavaApiFields.InstrID.value: instrument,
                'ListingList': {'ListingBlock': [{'ListingID': listing}]},
                JavaApiFields.Price.value: price})
            self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=18000)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_dma_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                'Verifying that DMA order is created (precondition and step (1))')
        except Exception as e:
            logger.error(f'Something gone wrong : {e}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 2: Filled DMA order
        self.execution_report.set_default_trade(child_dma_order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.OrdQty.value: qty,
            JavaApiFields.LastTradedQty.value: qty,
            JavaApiFields.LastPx.value: price,
            JavaApiFields.Price.value: price,
            JavaApiFields.LeavesQty.value: '0',
            JavaApiFields.CumQty.value: qty,
            JavaApiFields.AvgPrice.value: price})

        list_of_exec_id = []
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id,
                                                                                        child_care_order_id: child_care_order_id,
                                                                                        child_dma_order_id: child_dma_order_id})
        fee_amount = str(5 * (float(price) * float(qty)) / 100)
        execution_report = \
            self.java_api_manager.get_last_message_by_multiple_filter(ORSMessageType.ExecutionReport.value,
                                                                      [child_dma_order_id,
                                                                       ExecutionReportConst.ExecType_CAL.value]).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             execution_report,
                                             f'Verifying that {ExecutionReportConst.ExecType_CAL.value} execution of'
                                             f' {child_dma_order_id} has properly fees (step 2)')
        list_of_exec_id.append(self._check_that_executions_has_fees(child_dma_order_id, fee_amount))
        list_of_exec_id.append(execution_report[JavaApiFields.ExecID.value])
        list_of_exec_id.append(self._check_that_executions_has_fees(child_care_order_id, fee_amount))
        list_of_exec_id.append(self._check_that_executions_has_fees(order_id, fee_amount))
        # endregion

        # region step 3: send 35=8 39=3 message via BuyGateway
        self.ord_report_oms.set_default_done_for_day(
            self.execution_report.get_parameters()[JavaApiFields.ExecutionReportBlock.value], child_dma_order_id)
        self.java_api_manager.send_message(self.ord_report_oms)
        result = self._get_executions_id(child_dma_order_id)
        for index in range(2):
            self.java_api_manager.compare_values({JavaApiFields.ExecID.value: list_of_exec_id[index]},
                                                 {JavaApiFields.ExecID.value: result[index][0]},
                                                 f'Verify that {child_dma_order_id} has properly execution (step 3)')
        self.java_api_manager.compare_values({'CountExecution': '2'},
                                             {'CountExecution': str(len(result))},
                                             f'Verify that {child_dma_order_id} has only 2  executions (step 3)')

        result_for_child_co = self._get_executions_id(child_care_order_id)
        self.java_api_manager.compare_values({JavaApiFields.ExecID.value: list_of_exec_id[2]},
                                             {JavaApiFields.ExecID.value: result_for_child_co[0][0]},
                                             f'Verify that {child_care_order_id} has properly execution (step 3)')
        self.java_api_manager.compare_values({'CountExecution': '1'},
                                             {'CountExecution': str(len(result_for_child_co))},
                                             f'Verify that {child_care_order_id} has only 1  execution (step 3)')

        result_for_co_order = self._get_executions_id(order_id)
        self.java_api_manager.compare_values({JavaApiFields.ExecID.value: list_of_exec_id[3]},
                                             {JavaApiFields.ExecID.value: result_for_co_order[0][0]},
                                             f'Verify that {order_id} has properly execution (step 3)')
        self.java_api_manager.compare_values({'CountExecution': '1'},
                                             {'CountExecution': str(len(result_for_co_order))},
                                             f'Verify that {order_id} has only 1  execution (step 3)')

        for i in range(1, 4):
            fee_amt_actually = self._get_misc_fee_amt_of_execution(list_of_exec_id[i])
            self.java_api_manager.compare_values({JavaApiFields.MiscFeeAmt.value: fee_amount},
                                                 {JavaApiFields.MiscFeeAmt.value: str(fee_amt_actually)[:5]},
                                                 f'Verifying that {list_of_exec_id[i]} execution has properly fees (step 3)')

        # endregion

    def _set_fees(self):
        self.rest_commission_sender.clear_fees()
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('paris')
        self.rest_commission_sender.set_modify_fees_message(fee=fee)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
            'instrType': instr_type,
        })
        self.rest_commission_sender.send_post_request()

    def _check_that_executions_has_fees(self, order_id, fee_amount):
        execution_report = \
            self.java_api_manager.get_last_message_by_multiple_filter(ORSMessageType.ExecutionReport.value,
                                                                      [order_id,
                                                                       ExecutionReportConst.ExecType_TRD.value]).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        misc_fee_block = \
            execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][
                0]
        self.java_api_manager.compare_values({JavaApiFields.MiscFeeAmt.value: fee_amount},
                                             misc_fee_block,
                                             f'Verifying that {ExecutionReportConst.ExecType_TRD.value} execution of {order_id} has properly fees (step 2)')
        return execution_report[JavaApiFields.ExecID.value]

    def _get_executions_id(self, order_id):
        result = self.db_manager.execute_query(f"SELECT execid from execution WHERE transid = '{order_id}'")
        return result

    def _get_misc_fee_amt_of_execution(self, exec_id):
        result = self.db_manager.execute_query(f"SELECT miscfeeamt from execmiscfees WHERE execid = '{exec_id}'")
        return result[0][0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
