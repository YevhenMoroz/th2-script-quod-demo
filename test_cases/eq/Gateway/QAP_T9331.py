import logging
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
seconds, nanos = timestamps()


class QAP_T9331(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message.change_parameters({'Account': self.client})
        self.price = self.fix_message.get_parameter('Price')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_quickfixgtw_qfQuod_any_backoffice_sell.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_quickfixgtw_qfQuod_any_backoffice_sell.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region _recondition: Set up needed cfg:
        tree = ET.parse(self.local_path)
        element_1 = ET.fromstring('<onBehalfOfCompID>MIRA</onBehalfOfCompID>')
        element_2 = ET.fromstring('<onBehalfOfSubID>MIRA</onBehalfOfSubID>')
        element_3 = ET.fromstring('<deliverToCompID>MIRA</deliverToCompID>')
        element_4 = ET.fromstring('<deliverToSubID>MIRA</deliverToSubID>')
        quick_fix = tree.getroot().find('connectivity/quickfix')
        quick_fix.extend([element_1, element_2, element_3, element_4])
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart FIXBACKOFFICE_TH2")
        time.sleep(40)
        # endregion

        # region step 1-2: Create and Execute DMA order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check expected and actually results of step 1-2:
        list_of_ignore_fields = ['SecurityDesc', 'Text', 'LastMkt', 'SettlCurrency', 'StrategyParametersGrp',
                                 'ReplyReceivedTime', 'GatingRuleCondName', 'GatingRuleName',
                                 'BookID','QuodTradeQualifier','Parties','TradeReportingIndicator',
                                 'NoParty','tag5120','ExecBroker',
                                 'Account', 'TransactTime', 'SettlDate']
        checked_dict = {'OnBehalfOfCompID': 'MIRA',
                                            'DeliverToCompID': 'MIRA',
                                            'OnBehalfOfSubID': 'MIRA',
                                            'DeliverToSubID': 'MIRA'}
        self.fix_message.change_parameters(checked_dict)
        self.fix_verifier_dc.check_fix_message_fix_standard(self.fix_message, ['ClOrdID'],
                                                            ignored_fields=list_of_ignore_fields)
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        fix_execution_report.set_default_filled(self.fix_message)
        fix_execution_report.change_parameters(checked_dict)
        self.fix_verifier_dc.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart FIXBACKOFFICE_TH2")
        time.sleep(40)
        self.ssh_client.close()
