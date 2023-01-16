import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
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

seconds, nanos = timestamps()  # Test case start time


class QAP_T6919(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.qty = '500'
        self.price = '20'
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.alloc_account = self.data_set.get_account_by_name('client_pt_2_acc_2')
        self.client = self.data_set.get_client_by_name('client_pt_2')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_2_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up configuration on BackEnd(precondition)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/FIXNotif/mapping/ClientAccountGroupID/default").text = 'VenueClientAccountName'
        quod.find("ors/FIXNotif/mapping/ClientAccountGroupID/OrdReply").text = 'VenueClientAccountName'
        quod.find("ors/FIXNotif/mapping/ClientAccountGroupID/ExecutionReport").text = 'VenueClientAccountName'
        quod.find("ors/FIXNotif/mapping/ClientAccountGroupID/AllocationReport").text = 'AccountGroupID'
        quod.find("ors/FIXNotif/mapping/ClientAccountGroupID/Confirmation").text = 'AccountGroupID'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(90)
        # endregion

        # region Create CO order via FIX and execute it
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            # region create first DMA order
            no_allocs: dict = {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, 'Price': self.price, 'PreAllocGrp': no_allocs,
                 "Account": self.client})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check exec report in BO
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report,
                                                         ignored_fields=['Parties', 'QuodTradeQualifier', 'BookID',
                                                                         'NoParty', 'SecondaryOrderID', 'tag5120',
                                                                         'LastMkt', 'Text', 'ExecBroker'])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
