import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T11203(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_iceberg_limit()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.qty_to_display = '10'
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.qty = '100'
        self.price = '20'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create Algo order (Step 1)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'DisplayInstructionBlock': {'DisplayQty': self.qty_to_display, 'DisplayMethod': "Initial"}})
        nos_rule = None
        trade_rule1 = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.client_for_rule,
                self.mic,
                int(self.price))
            trade_rule1 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                             self.client_for_rule,
                                                                                             self.mic,
                                                                                             int(self.price),
                                                                                             int(int(self.qty_to_display) / 2), 0)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule1)
        ord_notif_reply = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        order_id = ord_notif_reply[JavaApiFields.OrdID.value]
        # endregion

        # region (Step 2)
        self.ssh_client.send_command("~/quod/script/site_scripts/db_endOfDay_postgres")
        status = self.db_manager.execute_query(f"select ordstatus from ordr where ordid='{order_id}';")[0][0]
        self.ja_manager.compare_values({"Sts": "EXP"}, {"Sts": status}, "Check order status")
        # endregion
