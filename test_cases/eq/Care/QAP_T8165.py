import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8165(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_dummy')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = os.path.abspath("test_framework\ssh_wrappers\oms_cfg_files\client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Setup ORS
        tree = ET.parse(self.local_path)
        root = tree.getroot()
        root.find("ors/FrontToBack/UnknownInstrument/dummy").text = "false"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion
        # region Step 1
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id: str = response[0].get_parameter('OrderID')
        bool_value = order_id.startswith('RO')
        self.order_book.compare_values({"OrdStatus": "8", "ExecType": "8", 'BookValueForOrderID': True},
                                       {"OrdStatus": response[0].get_parameter('OrdStatus'),
                                        "ExecType": response[0].get_parameter('ExecType'),
                                        'BookValueForOrderID': bool_value}, "Compare order sts and order id")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
