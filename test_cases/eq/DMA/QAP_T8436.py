import logging
import os
import time
from copy import copy
from pathlib import Path
import xml.etree.ElementTree as ET

from pkg_resources import resource_filename

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


class QAP_T8436(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.instrument = self.data_set.get_fix_instrument_by_name('instrument_1')
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.price = self.fix_message.get_parameter('Price')
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up configuration on BackEnd(precondition)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/FrontToBack/instrTypeFilter").text = "true"
        quod.find("ors/FrontToBack/currencyFilter").text = 'true'
        quod.find("ors/FrontToBack/listingCurrencyFilter").text = "true"
        quod.find("ors/FrontToBack/exDestinationFilter").text = 'true'
        quod.find("ors/FrontToBack/venueFilter").text = "true"
        quod.find("ors/FrontToBack/isinFilter").text = 'false'
        quod.find("ors/FrontToBack/enforceRoute").text = "false"
        quod.find("ors/FrontToBack/securityExchangeFilter/default").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(90)
        # endregion

        # region Create order
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            # region create first DMA order
            instr = copy(self.instrument)
            self.instrument.pop('SecurityExchange')
            self.fix_message.change_parameters({"Instrument": self.instrument, 'ExDestination': self.venue})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # endregion
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check exec report
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters({"Instrument": instr})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report,
                                                         ignored_fields=['ReplyReceivedTime', 'SecondaryOrderID',
                                                                         'LastMkt', 'Text', "GatingRuleCondName",
                                                                         "GatingRuleName"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
        time.sleep(90)
