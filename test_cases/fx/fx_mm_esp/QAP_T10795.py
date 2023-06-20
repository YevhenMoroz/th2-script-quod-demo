import os
import re
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T10795(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.temp_path = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'th2-script-quod-demo', 'temp')
        self.verifier = Verifier()
        self.key = None
        self.result = str()
        self.order_id = str()
        self.pass_amount = int()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        response = self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value,
                                                           "ExecMiscBlock").get_parameter(
                                                           JavaApiFields.ExecutionReportBlock.value)
        self.order_id = response["ClOrdID"]
        self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.ORS.log", rf"^.*no Transac with keys.*{self.order_id}.*$")
        if not self.result:
            self.pass_amount += 1
        # endregion
        # region Step 1
        self.trade_request.set_default_params()
        response = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                           "ExecMiscBlock").get_parameter(
                                                           JavaApiFields.ExecutionReportBlock.value)
        self.order_id = response["ClOrdID"]
        self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.ORS.log", rf"^.*no Transac with keys.*{self.order_id}.*$")
        if not self.result:
            self.pass_amount += 1
        # endregion
        # region Step 1
        self.trade_request.set_default_params()
        response = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                           "ExecMiscBlock").get_parameter(
                                                           JavaApiFields.ExecutionReportBlock.value)
        self.order_id = response["ClOrdID"]
        self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.ORS.log", rf"^.*no Transac with keys.*{self.order_id}.*$")
        if not self.result:
            self.pass_amount += 1
        if self.pass_amount != 3:
            self.result = "failed"
        else:
            self.result = "pass"
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check that there is no Cache checks while Trade Transacs")
        self.verifier.compare_values("status", "pass", self.result)
        self.verifier.verify()
        # endregion
