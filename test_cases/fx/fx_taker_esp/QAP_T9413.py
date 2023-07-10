from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixMarketDataRequestFX import FixMarketDataRequestFX
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T9413(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.md_request = FixMarketDataRequestFX()
        self.verifier = Verifier(self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.result = bool()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_default_taker_sub()
        self.java_api_manager.send_message(self.md_request)
        md_req_id = self.md_request.get_parameter("MarketDataRequestBlock")["MDReqID"]
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.MDA.log",
                                                         rf"^.*AuthenticationBlock.*{md_req_id}.*$")
        if self.result:
            self.result = "True"
        self.verifier.set_event_name("AuthenticationBlock check")
        self.verifier.compare_values("AuthenticationBlock is present in fix MD Request", "True", self.result)
        self.verifier.verify()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.unsubscribe()
        self.java_api_manager.send_message(self.md_request)
