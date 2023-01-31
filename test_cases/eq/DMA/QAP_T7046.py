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
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7046(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client = self.data_set.get_client_by_name('client_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_quickfixgtw_qfQuod_any_backoffice_sell.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_quickfixgtw_qfQuod_any_backoffice_sell.xml"
        self.local_path2 = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path2 = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        tree.getroot().find("connectivity/mapClientAccountGroupIDForTavira").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        tree = ET.parse(self.local_path2)
        tree.getroot().find("ors/FIXNotif/mapping/ClientAccountGroupID/OrdReply").text = 'RouteSecActName'
        tree.getroot().find("ors/FIXNotif/mapping/ClientAccountGroupID/ExecutionReport").text = 'RouteSecActName'
        tree.getroot().find("ors/FIXNotif/mapping/ClientAccountGroupID/default").text = 'RouteSecActName'
        tree.write("temp2.xml")
        self.ssh_client.put_file(self.remote_path2, "temp2.xml")
        self.ssh_client.send_command("qrestart ORS FIXBACKOFFICE_TH2")
        time.sleep(40)
        # endregion
        # region Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, int(self.price),
                                                                                          int(self.qty), 1)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"Account": self.client}, exec_rep, "Check Client in sell gtw report")
        self.fix_message.update_fields_in_component("Instrument", {"SecurityExchange": self.mic})
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.remove_parameters(['TradeReportingIndicator', 'Parties', 'SettlCurrency'])
        ignored_fields = ["QuodTradeQualifier", "BookID", "NoParty", "tag5120", "LastMkt", "Text", "ExecBroker"]
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.put_file(self.remote_path2, self.local_path2)
        self.ssh_client.send_command("qrestart ORS FIXBACKOFFICE_TH2")
        time.sleep(20)
        os.remove("temp.xml")
        os.remove("temp2.xml")
