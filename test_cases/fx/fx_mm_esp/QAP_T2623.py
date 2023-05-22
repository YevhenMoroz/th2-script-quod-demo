import os
import re
import time
from pathlib import Path
from pkg_resources import resource_filename
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.ssh_wrappers.ssh_client import SshClient
from xml.etree.ElementTree import parse as parse_xml


class QAP_T2623(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportFX()
        # region SSH
        self.config_file = "client_qf_kharkiv_quod7_th2.xml"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/{self.config_file}"
        self.temp_path = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'th2-script-quod-demo', 'temp')
        # endregion
        self.result = None
        self.tree = None
        self.key = None
        self.qs = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_md_req_parameters_maker()
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3
        self.new_order_single.set_default()
        response = self.fix_manager.send_message_and_receive_response(self.new_order_single, self.test_id)
        order_id = response[-1].get_parameter("OrderID")
        self.execution_report.set_params_from_new_order_single(self.new_order_single, response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report)
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
                                                         rf"^.*{order_id}.*ClientAccountGroupID=.Silver1.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "Silver1 haven't mapped in ClientAccountGroupID, it's most likely a bug"
        # self.ssh_client.get_file("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
        #                          self.temp_path)
        # logs = open(self.temp_path, "r")
        # self.result = "Silver1 haven't mapped in ClientAccountGroupID, it's most likely a bug"
        # for line in logs:
        #     self.key = re.findall(rf"^.*{order_id}.*ClientAccountGroupID=.Silver1.*$", line)
        #     if self.key:
        #         self.result = "ok"
        #         break

        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"ClientAccountGroupID\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        # logs.close()
        # os.remove(self.temp_path)
        # endregion
        # region precondition: Prepare QS configuration
        self.tree = parse_xml(self.local_path)
        self.qs = self.tree.getroot().find("connectivity/quickfix/mapClientAccount/tagList/tag")
        self.qs.text = '49'
        self.tree.write("temp.xml", encoding="ISO-8859-1")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QS_ESP_FIX_TH2")
        time.sleep(85)
        # endregion
        # region Step 1
        self.md_request.set_md_req_parameters_maker()
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3
        self.new_order_single.set_default()
        response = self.fix_manager.send_message_and_receive_response(self.new_order_single, self.test_id)
        order_id = response[-1].get_parameter("OrderID")
        self.execution_report.set_params_from_new_order_single(self.new_order_single, response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report)

        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
                                                         rf"^.*{order_id}.*ClientAccountGroupID=.Silver1.*$")
        if self.result:
            self.result = "ok"
        else:
            self.result = "Silver1 haven't mapped in ClientAccountGroupID, it's most likely a bug"
        # self.ssh_client.get_file("/Logs/quod314/QUOD.QS_ESP_FIX_TH2.log",
        #                          self.temp_path)
        # logs = open(self.temp_path, "r")
        # self.result = "QUOD7 haven't mapped in ClientAccountGroupID, it's most likely a bug"
        # for line in logs:
        #     self.key = re.findall(rf"^.*{order_id}.*ClientAccountGroupID=.QUOD7.*$", line)
        #     if self.key:
        #         self.result = "ok"
        #         break
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check \"ClientAccountGroupID\" tag")
        self.verifier.compare_values("status", "ok", self.result)
        self.verifier.verify()
        # logs.close()
        # os.remove(self.temp_path)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager.send_message(self.md_request)
        self.qs.text = '1'
        self.tree.write("temp.xml", encoding="ISO-8859-1")
        self.ssh_client.send_command('~/automation_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QS_ESP_FIX_TH2")
        self.ssh_client.close()
        time.sleep(85)
