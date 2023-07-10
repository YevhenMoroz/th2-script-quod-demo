import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8616(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_modification_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.order_cancel_request = FixMessageOrderCancelRequestOMS()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_cs = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path_cs = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.new_price = '44'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree_cs = ET.parse(self.local_path_cs)
        tree_cs.getroot().find("cs/fixAutoAcknowledge").text = 'false'
        tree_cs.getroot().find("cs/fixAutoAckNewOrderEvenIfRecipientNotConnected").text = 'false'
        tree_cs.write("temp_cs.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path_cs, "temp_cs.xml")
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(60)
        # endergion

        # region  precondition : create CO order via FIX (step 1)
        self.new_order.set_default_care_limit(account="client_pt_1")
        response1 = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order)
        new_execution_report = response1[0].get_parameters()
        self.java_api_manager.compare_values({'OrdStatus': '0'}, new_execution_report, 'Check order after creation')
        # endregion

        # region send OrderCancelReplaceRequest (step 2)
        self.order_modification_request.set_default(self.new_order, price=self.new_price)
        self.fix_manager.send_message_and_receive_response_fix_standard(self.order_modification_request)
        replace_exec_report = self.fix_manager.get_last_message('ExecutionReport', "'ExecType': '5'").get_parameters()
        self.java_api_manager.compare_values({'OrdStatus': '5', 'Price': self.new_price}, replace_exec_report,
                                             'Check values after CancelReplaceRequest')
        # endregion

        # region send OrderCancelRequest (step 3)
        self.order_cancel_request.set_default(self.new_order)
        self.fix_manager.send_message_and_receive_response_fix_standard(self.order_cancel_request)
        cancel_response = self.fix_manager.get_last_message('ExecutionReport', "'ExecType': '4'").get_parameters()
        self.java_api_manager.compare_values({'OrdStatus': '4'}, cancel_response,
                                             'Check values after CancelReplaceRequest')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path_cs, self.local_path_cs)
        self.ssh_client.send_command("qrestart QUOD.CS")
        os.remove('temp_cs.xml')
        time.sleep(60)
        self.ssh_client.close()
