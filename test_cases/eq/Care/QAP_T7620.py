import logging
import time
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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst, \
    SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def _get_fix_message(parameter: dict, responses):
    for i in range(len(responses)):
        for j in parameter.keys():
            if responses[i].get_parameters()[j] == parameter[j]:
                return responses[i].get_parameters()


class QAP_T7620(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.account = self.fix_message.get_parameter('Account')
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_action_request = OrderActionRequest()
        self.order_submit_request = OrderSubmitOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-2 create CO order
        order_qty = '30000'
        order_price = '5'
        self.fix_message.change_parameters({"Price": order_price,
                                            'OrderQtyData': {'OrderQty': order_qty},
                                            "Side": "2"})
        responses: list = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = responses[0].get_parameter("OrderID")
        cl_ord_id = responses[0].get_parameter("ClOrdID")
        expected_result = {'OrdStatus': '0'}
        last_response = _get_fix_message(expected_result, responses)
        self.java_api_manager.compare_values(expected_result, last_response,
                                             'Checking actually and expected result (step 2)')
        # endregion

        # region step 3 : Set DiscloseExec = Manual
        self.order_action_request.set_default([order_id])
        order_dict = {order_id: order_id}
        self.java_api_manager.send_message_and_receive_response(self.order_action_request, order_dict)
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id). \
            get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value},
            order_notification, f'Verifying that DiscloseExec = M for {order_id} (step 3)')
        # endregion

        # region step 4-5: Split CO order
        listing = self.data_set.get_listing_id_by_name("listing_3")
        instrument = self.data_set.get_instrument_id_by_name("instrument_2")
        first_split_qty = '20000'
        exec_id = self._split_co_order_and_trade(order_id, order_price, self.client_for_rule,
                                                 listing, instrument, first_split_qty, ['step 4', 'step 5'])
        # endregion

        # region step 6-7 : Send Execution Summary first time
        self.trade_entry_request.set_default_execution_summary(order_id, [exec_id], order_price, first_split_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request, order_dict)

        # region step 7: Check ExecutionReport (39=B)
        self._check_fix_message(order_price, order_price)
        # endregion

        # region step 8-9: Split CO order second time
        second_split_qty = '10000'
        exec_id = self._split_co_order_and_trade(order_id, order_price, self.client_for_rule,
                                                 listing, instrument, second_split_qty, ['step 8', 'step 9'])
        # endregion

        # region step 10: Send Execution Summary second time
        second_price = '20'
        self.trade_entry_request.set_default_execution_summary(order_id, [exec_id], second_price, second_split_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request, order_dict)
        # endregion

        # region step 11: Check ExecutionReport (39=B)
        avg_px = int(
            (int(first_split_qty) * int(order_price) + int(second_split_qty) * int(second_price)) / int(order_qty))
        self._check_fix_message(avg_px, second_price)
        # endregion

    def _split_co_order_and_trade(self, order_id, price, client_for_rule, listing,
                                  instrument, qty, step: list):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(price),
                                                                                            int(qty), delay=0)
            self.order_submit_request.set_default_child_dma(order_id)
            self.order_submit_request.update_fields_in_component('NewOrderSingleBlock', {'Price': price,
                                                                                         'OrdQty': qty,
                                                                                         'Side': SubmitRequestConst.Side_Sell.value,
                                                                                         'InstrID': instrument,
                                                                                         'ListingList': {'ListingBlock':
                                                                                             [{
                                                                                                 'ListingID': listing}]}
                                                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit_request)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                 f"'TransStatus': '{OrderReplyConst.TransStatus_OPN.value}'").get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                f'Checking that Child DMA order created {step[0]}')
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            exec_id = execution_report[JavaApiFields.ExecID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, f"Verifying that CO order {order_id} filled ({step[1]})")
            return exec_id
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

    def _check_fix_message(self, avg_px, last_px):
        ignored_fields = ['GatingRuleName', 'GatingRuleCondName', 'trailer', 'header', 'LastMkt', 'TradeDate']
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters(
            {"AvgPx": avg_px, "Account": self.account, "Side": "2", "VenueType": "*", 'LastPx': last_px})
        self.fix_verifier.check_fix_message(self.exec_report, ['ClOrdID', 'OrdStatus', 'ExecType', 'AvgPx'],
                                            ignored_fields=ignored_fields)
