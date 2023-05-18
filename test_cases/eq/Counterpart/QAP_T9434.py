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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst, \
    SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9434(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_verifier_bs = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_4")
        self.alloc_account = self.data_set.get_account_by_name('client_counterpart_4_acc_1')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_4_venue_1")
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.user_1 = self.environment.get_list_fe_environment()[0].user_1
        self.user_2 = self.environment.get_list_fe_environment()[0].user_2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set needed counterparts:
        counter_part_for_user_1 = self.data_set.get_counterpart_id_java_api('counterpart_executing_trader')
        counter_part_for_user_2 = self.data_set.get_counterpart_id_java_api('counterpart_executing_trader_2')
        self._set_new_counterparts_for_account_and_client(counter_part_for_user_1[
                                                              JavaApiFields.CounterpartID.value], self.user_1)
        self._set_new_counterparts_for_account_and_client(counter_part_for_user_2[
                                                              JavaApiFields.CounterpartID.value], self.user_2)
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)
        # endregion

        # region step 1: create CO order:
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=15000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply, 'Verify that order created and has properly status (step 1)')
        result = counter_part_for_user_1 in order_reply[JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        self.java_api_manager.compare_values({'ConterpartIsPresent': True},
                                             {'ConterpartIsPresent': result},
                                             'Verify that Order has counterpart from user (step 1)')
        # endregion

        # region step 2: Trade CO order
        self.trade_entry.set_default_trade(order_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry, response_time=15000)
        execution_report = \
        self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            'Verifying that Order filled (step 2))')
        # endregion

        # region step 3: Cancel Execution Trade
        self.trade_entry.set_default_cancel_execution(order_id, exec_id)
        self.java_api_manager2.send_message_and_receive_response(self.trade_entry)
        execution_report = \
            self.java_api_manager2.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]

        self.java_api_manager2.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
            execution_report, 'Verify that execution has ExecStatus = TradeCancel (step 3)')
        # endregion

    def _set_new_counterparts_for_account_and_client(self, counterpart_id_user, user):
        self.db_manager.execute_query(
            f"UPDATE userlogin SET counterpartid = '{counterpart_id_user}' WHERE userid = '{user}'")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        counter_part_for_user_1 = self.data_set.get_counterpart_id_java_api('counterpart_custodian_user')[
            JavaApiFields.CounterpartID.value]
        counter_part_for_user_2 = self.data_set.get_counterpart_id_java_api('counterpart_custodian_user_2')[
            JavaApiFields.CounterpartID.value]
        self._set_new_counterparts_for_account_and_client(counter_part_for_user_1, self.user_1)
        self._set_new_counterparts_for_account_and_client(counter_part_for_user_2, self.user_2)
        self.ssh_client.send_command("qrestart all")
        time.sleep(140)
