import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename

import xml.etree.ElementTree as ET
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


class QAP_T8437(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message.remove_parameter('Currency')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # MOClient_PARIS
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<idGen><instrument><instrCurrency>true</instrCurrency></instrument></idGen>")
        quod = tree.getroot()
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        # endregion
        # region Step 1
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(self.price))
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
            self.fix_manager.compare_values(
                {"OrdStatus": "0", "Currency": self.data_set.get_currency_by_name("currency_1")}
                , exec_rep, "Check OrdStatus and Currency")
        except Exception as e:
            logger.error(f'Something go wrong via {e}')
        finally:
            self.rule_manager.remove_rule(new_order_single)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        os.remove("temp.xml")
