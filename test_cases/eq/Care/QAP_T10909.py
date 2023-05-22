import logging
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, SubmitRequestConst, \
    OrderReplyConst, ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10909(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_action_request = OrderActionRequest()
        self.order_submit_request = OrderSubmitOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        self.order_submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                         desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                         role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value
        })
        price = self.order_submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.Price.value]
        qty = self.order_submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.OrdQty.value]
        self.java_api_manager.send_message_and_receive_response(self.order_submit_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id). \
            get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value},
                                             order_notification, f'Verify that order has '
                                                                 f'{JavaApiFields.DiscloseExec.value} = M (step 1)')
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply,
                                             'Verify that order created (step 1)')
        # endregion

        # region step 2-3: Create and trade Split DMA order
        open_rule = trade_rule = None
        half_qty = str(int((int(qty) / 2)))
        try:
            open_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.exec_destination,
                int(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            int(price),
                                                                                            int(half_qty), 2)
            self.order_submit_request.set_default_child_dma(order_id)
            self.order_submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                                 {JavaApiFields.OrdQty.value: half_qty})
            self.java_api_manager.send_message_and_receive_response(self.order_submit_request)
            execution_report_child = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                            f"'ExecutionPolicy': '{ExecutionPolicyConst.DMA.value}'").get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report_child, 'Verify that DMA order is filled (step 3)')
        except Exception as e:
            logger.error(f'Exception {e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(open_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 4: Perform Execution Summary
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.trade_entry_request.set_default_execution_summary(order_id, [exec_id], price, half_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request, {order_id: order_id})
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             execution_report,
                                             'Verify that new Calculated execution was created(step 4)')
        # endregion

        # region step 5: Manual Execute CO order
        manual_exeucte_qty = '10'
        self.trade_entry_request.set_default_trade(order_id, price, manual_exeucte_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = \
            self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.ExecQty.value: str(float(manual_exeucte_qty))},
            execution_report, 'Verify that new Execution created (step 5)')
        # endregion

        # region step 6: Create Child DMA order again
        try:
            open_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.exec_destination,
                int(price))
            self.order_submit_request.set_default_child_dma(order_id)
            self.order_submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                                 {JavaApiFields.OrdQty.value: str(
                                                                     float(manual_exeucte_qty))})
            self.java_api_manager.send_message_and_receive_response(self.order_submit_request)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                 ExecutionPolicyConst.DMA.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Verify that DMA order is created (step 6)')
        except Exception:
            bca.create_event("TEST FAILED", self.test_id,
                             status='FAILED')
            exc_traceback = sys.exc_info()[2]
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(open_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
