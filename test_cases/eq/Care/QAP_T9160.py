import logging
import os
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
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9160(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.new_order_single.get_parameter('Price')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.suspend_order = SuspendOrderManagementRequest()
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition : create CO order
        # region create orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = response[0].get_parameter("OrderID")
        # endregion

        # create Child Care order
        self.order_submit.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                 self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 SubmitRequestConst.USER_ROLE_1.value, order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.RootParentOrdID.value: order_id},
            order_notif, 'Check child Care order')
        child_care_id = order_notif['OrdID']
        # endregion

        # create Child DMA order
        nos_rule = None
        exec_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            exec_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                           self.client_for_rule,
                                                                                           self.mic,
                                                                                           float(self.price),
                                                                                           int(self.qty), 0)
            self.order_submit.set_default_child_dma(child_care_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                exec_report, 'Check child order exec sts')
            order_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.RootParentOrdID.value: order_id},
                order_notif, 'Check child DMA order')
        finally:
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(exec_rule)
        # endregion

        # check BO
        ignored_list = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                        'TradeReportingIndicator', 'NoParty', 'tag5120', 'LastMkt', 'LastMkt', 'ExecBroker']
        self.exec_report.set_default_filled(self.new_order_single)
        self.exec_report.change_parameters({'OrderID': order_id, 'SecondaryOrderID': child_care_id})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion

        # complete order
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        # endregion

        # check BO
        ignored_list.extend(
            ['SettlCurrency', 'LastExecutionPolicy', 'TradeDate', 'SecondaryExecID'])
        self.exec_report.set_default_calculated(self.new_order_single)
        self.exec_report.change_parameters({'OrderID': order_id})
        self.exec_report.remove_parameters(['SecondaryOrderID'])
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion
