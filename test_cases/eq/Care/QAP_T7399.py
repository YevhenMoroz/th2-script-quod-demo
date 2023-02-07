import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, SubmitRequestConst, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.java_api_wrappers.ors_messages.TradeEntryBatchRequest import TradeEntryBatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7399(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.account = self.fix_message.get_parameter('Account')
        self.price_sum = "22.2"
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_action_request = OrderActionRequest()
        self.order_submit_request = OrderSubmitOMS(self.data_set)
        self.trade_entry_batch_request = TradeEntryBatchRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : create CO orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response[0].get_parameter("OrderID")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response[0].get_parameter("OrderID")
        # endregion

        # region step 2: Set DiscloseFlag = M to orders
        orders_id = [order_id1, order_id2]
        self.order_action_request.set_default(orders_id)
        order_dict = {order_id1: order_id1, order_id2: order_id2}
        self.java_api_manager.send_message_and_receive_response(self.order_action_request, order_dict)
        for order_id in orders_id:
            order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.DiscloseExec.value:OrderReplyConst.DiscloseExec_M.value},
                                                 order_notification, f'Verifying that DiscloseExec = M for {order_id} (step 2)')
        # endregion

        # region step  3 : Split and Execute CO orders
        listing_1 = self.data_set.get_listing_id_by_name("listing_3")
        instrument_1 = self.data_set.get_instrument_id_by_name("instrument_2")
        exec_ids_list = []
        for order_id in orders_id:
            exec_ids_list.append(
                self.__split_co_order_and_trade(order_id, self.price, self.client_for_rule,
                                                self.account,
                                                SubmitRequestConst.Side_Buy.value, listing_1, instrument_1))

        # region step 4-6: Send Mass Exec Summary
        self.trade_entry_batch_request.set_orders_and_exec_id(order_id1, [exec_ids_list[0]], self.price_sum, self.qty)
        self.trade_entry_batch_request.set_orders_and_exec_id(order_id2, [exec_ids_list[1]], self.price_sum, self.qty)
        self.trade_entry_batch_request.set_default()
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_batch_request, order_dict)
        # endregion

        # region step 7: Check ExecutionReports(39=B)
        ignored_fields = ['GatingRuleName', 'GatingRuleCondName', 'trailer', 'header']
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({"LastPx": self.price_sum, "VenueType": "*", 'OrderID': order_id1})
        self.fix_verifier.check_fix_message(self.exec_report, ['OrderID', 'ExecType'], ignored_fields=ignored_fields)
        self.exec_report.change_parameters({'OrderID': order_id2})
        self.fix_verifier.check_fix_message(self.exec_report, ['OrderID', 'ExecType'], ignored_fields=ignored_fields)
        # endregion

    def __split_co_order_and_trade(self, order_id, price, client_for_rule, client, side, listing,
                                   instrument):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                self.exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(price),
                                                                                            int(self.qty), delay=0)
            self.order_submit_request.set_default_child_dma(order_id)
            self.order_submit_request.update_fields_in_component('NewOrderSingleBlock', {'Price': price,
                                                                                         'OrdQty': self.qty,
                                                                                         'AccountGroupID': client,
                                                                                         'Side': side,
                                                                                         'InstrID': instrument,
                                                                                         'ListingList': {
                                                                                             'ListingBlock':
                                                                                                 [{
                                                                                                     'ListingID': listing}]}
                                                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit_request)
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            exec_id = execution_report[JavaApiFields.ExecID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, f"Verifying that CO order {order_id} filled (step 3)")
            return exec_id
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
