import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecsToParentOrderRequest import \
    ManualMatchExecsToParentOrderRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionPolicyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7421(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_1")
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.account = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.manual_match = ManualMatchExecsToParentOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verifying that CO order created (step 1)')
        # endregion

        # region step 2: Create DMA order and partially filled its
        qty = self.order_submit.get_parameter('NewOrderSingleBlock')[JavaApiFields.OrdQty.value]
        account = self.order_submit.get_parameter('NewOrderSingleBlock')[JavaApiFields.AccountGroupID.value]
        price = self.order_submit.get_parameter('NewOrderSingleBlock')[JavaApiFields.Price.value]
        dma_order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.account,
                                                                                                  self.mic,
                                                                                                  float(price))
            self.order_submit.get_parameters().clear()
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"ClOrdID": bca.client_orderid(9),
                                                                                 JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            dma_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                'Verifying that DMA order is created (step 2)')
        except Exception as e:
            logger.error(f'Something gone wrong : {e}', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 3: Partially Filled DMA order
        self.execution_report.set_default_trade(dma_order_id)
        first_qty = str(float(int(qty) / 2) - 10)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "OrdQty": qty,
            "LastTradedQty": first_qty,
            "LastPx": price,
            "Price": price,
            "LeavesQty": first_qty,
            "CumQty": first_qty,
            "AvgPrice": price})
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_1 = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verifying that DMA order is partially filled (step 3)')
        # endregion

        # region step 4: Partially Filled DMA order
        second_qty = str(float(qty) - float(first_qty))
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "VenueExecID": bca.client_orderid(9),
            "CumQty": second_qty,
            "LastTradedQty": second_qty,
            "LeavesQty": '0'
        })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_2 = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verifying that DMA order is filled (step 4)')
        # endregion

        # region step 5-7: Manual Match N to 1
        exec_ids = [exec_id_1, exec_id_2]
        qty_list = [first_qty, second_qty]
        self.manual_match.set_default_match_to_n(order_id, exec_ids, qty_list)
        self.java_api_manager.send_message_and_receive_response(self.manual_match)
        for qty in qty_list:
            execution = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, qty).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            exec_id = execution[JavaApiFields.ExecID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value}, execution,
                f'Verifying that {exec_id} has ExeType = Trade (step 7)')
            if qty == first_qty:
                self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: '0.0',
                                                      JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                                                     execution,
                                                     'Verifying that CO order has properly properties (step 7)')
        # endregion
