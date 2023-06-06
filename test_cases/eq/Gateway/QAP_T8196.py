import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, QtyPercentageProfile, \
    OrdListNotificationConst, ExecutionReportConst
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8196(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListFromExistingOrders()
        self.wave_creation_request = OrderListWaveCreationRequest()
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.new_order_single.get_parameter('Price')
        self.fix_verifier_sell = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_back_office = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.basket_name = 'Basket_QAP_T8196'
        self.qty = '100'
        self.price = '20'
        self.qty_percent1 = '0.5'
        self.qty_percent2 = '1.0'
        self.qty_of_wave = '50'
        self.fix_exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create orders (precondition)
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id1 = response[0].get_parameter("OrderID")
        cl_order_id1 = response[0].get_parameter("ClOrdID")
        self.new_order_single.change_parameters(
            {'ClOrdID': basic_custom_actions.client_orderid(9)})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id2 = response[0].get_parameter("OrderID")
        cl_order_id2 = response[0].get_parameter("ClOrdID")
        # endregion

        # step 1
        # region create basket
        self.list_creation_request.set_default([order_id1, order_id2], self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameter(
                JavaApiFields.NewOrderListReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status (step 1)')
        list_id = list_notify_block[JavaApiFields.OrderListID.value]
        # endregion

        # region Wave basket (2-4)
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty_of_wave),
                                                                                            2)
            self.wave_creation_request.set_default(list_id, ord_id_list=[order_id1, order_id2],
                                                   percent_qty=self.qty_percent1)
            self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        wave_notif_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            JavaApiFields.OrderListWaveNotificationBlock.value)
        # endregion

        # region Verify wave
        self.java_api_manager.compare_values(
            {JavaApiFields.QtyPercentageProfile.value: QtyPercentageProfile.RemainingQty.value,
             JavaApiFields.PercentQtyToRelease.value: self.qty_percent1},
            wave_notif_block,
            'Check created first wave (step 2)')
        # endregion

        # region Verify child orders
        ord_notify_element = wave_notif_block['OrdNotificationElements']['OrdNotificationBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty_of_wave + '.0', JavaApiFields.RootParentOrdID.value: order_id1,
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            ord_notify_element[0],
            'Check first Child Order after first waving (step 3)')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty_of_wave + '.0', JavaApiFields.RootParentOrdID.value: order_id2,
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            ord_notify_element[1],
            'Check second Child Order after first waving (step 3)')
        # endregion

        ignored_fields = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                          'SettlCurrency', 'ReplyReceivedTime', 'Account',
                          'TradeReportingIndicator', 'NoParty', 'SecondaryOrderID', 'tag5120', 'LastMkt',
                          'ExecBroker', 'header', 'trailer']

        # region check execution report on the BO (step 5)
        self.fix_exec_report.set_default_filled(self.new_order_single)
        self.fix_exec_report.change_parameters(
            {"ClOrdID": cl_order_id1, "OrdStatus": "1", 'OrderListName': self.basket_name})
        self.fix_verifier_back_office.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id2})
        self.fix_verifier_back_office.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        # endregion

        # region check execution report on the Sell Side (step 6)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id1})
        self.fix_verifier_sell.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id2})
        self.fix_verifier_sell.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        # endregion

        # region second time Wave basket (7-8)
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty_of_wave),
                                                                                            2)
            self.wave_creation_request.set_default(list_id, ord_id_list=[order_id1, order_id2],
                                                   percent_qty=self.qty_percent2)
            self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        wave_notif_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            JavaApiFields.OrderListWaveNotificationBlock.value)
        # endregion

        # region Verify wave
        self.java_api_manager.compare_values(
            {JavaApiFields.QtyPercentageProfile.value: QtyPercentageProfile.RemainingQty.value,
             JavaApiFields.PercentQtyToRelease.value: self.qty_percent2},
            wave_notif_block,
            'Check created first wave (step 7)')
        # endregion

        # region Verify child orders
        ord_notify_element = wave_notif_block['OrdNotificationElements']['OrdNotificationBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty_of_wave + '.0', JavaApiFields.RootParentOrdID.value: order_id1},
            ord_notify_element[0],
            'Check first Child Order after second waving (step 8)')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty_of_wave + '.0', JavaApiFields.RootParentOrdID.value: order_id2},
            ord_notify_element[1],
            'Check second Child Order after second waving (step 8)')
        # endregion

        # region check execution report on the BO (step 9)
        self.fix_exec_report.set_default_filled(self.new_order_single)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id1, 'OrderListName': self.basket_name})
        self.fix_verifier_back_office.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id2})
        self.fix_verifier_back_office.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        # endregion

        # region check execution report on the Sell Side (step 10)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id1})
        self.fix_verifier_sell.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        self.fix_exec_report.change_parameters({"ClOrdID": cl_order_id2})
        self.fix_verifier_sell.check_fix_message(self.fix_exec_report, key_parameters=['ClOrdID', 'OrdStatus'],
                                                        ignored_fields=ignored_fields)
        # endregion
