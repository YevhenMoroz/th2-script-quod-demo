import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6914(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<clientAccountGroupConversion>true</clientAccountGroupConversion>")
        quod = tree.getroot().find("ors/FrontToBack")
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion
        # region Step 1
        try:
            rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(self.price))
            client = self.data_set.get_client_by_name("client_pt_1").upper()
            account = self.data_set.get_account_by_name('client_pt_1_acc_1').upper()
            no_allocs = {"NoAllocs": [{'AllocAccount': account, 'AllocQty': self.qty}]}
            self.fix_message.change_parameters({"Account": client, "PreAllocGrp": no_allocs})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(rule)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"Account": self.client, "OrdStatus": "A"}, exec_rep, "Check Client")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        os.remove("temp.xml")
