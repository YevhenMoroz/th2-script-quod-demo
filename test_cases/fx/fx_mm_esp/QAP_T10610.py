import os
import re
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import execute_db_command
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T10610(TestCase):
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
        self.turn_off_permission = f"UPDATE permrolemessage SET alive = 'N' " \
                              f"WHERE permroleid='10011' and messagename='Order_TradeEntryRequest';"
        self.turn_on_permission = f"UPDATE permrolemessage SET alive = 'Y' " \
                              f"WHERE permroleid='10011' and messagename='Order_TradeEntryRequest';"
        self.verifier = Verifier()
        self.key = None
        self.result = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 3
        execute_db_command(self.turn_off_permission)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
        # endregion
        # region Step 1
        self.trade_request.set_default_params()
        response = self.java_api_manager.send_message_and_receive_response(self.trade_request)[0].get_parameters()
        message_id = response["TechnicalHeaderBlock"]["MessageID"]
        self.ssh_client.get_file("/Logs/quod314/QUOD.ORS.log",
                                 self.temp_path)
        logs = open(self.temp_path, "r")
        self.result = "failed"
        for line in logs:
            self.key = re.findall(rf"^.*{message_id}.*permission denied.*$", line)
            if self.key:
                self.result = "pass"
                break
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check that Trade Entry Request is rejected")
        self.verifier.compare_values("status", "pass", self.result)
        self.verifier.verify()
        logs.close()
        os.remove(self.temp_path)
        # endregion

    @ try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        execute_db_command(self.turn_on_permission)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
