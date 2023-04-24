import logging
import os
import re
import time
from copy import deepcopy
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9034(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.price = self.fix_message.get_parameter("Price")
        self.rule_manager = RuleManager(Simulators.equity)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.manual_execute = TradeEntryOMS(self.data_set)
        self.account = self.data_set.get_client_by_name("client_counterpart_1")
        self.price = self.fix_message.get_parameter('Price')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<TradeCapture><autoCreation><enabled>true</enabled>"
                                "<venues><PARIS><enabled>true</enabled>""</PARIS></venues>"
                                "</autoCreation><sendToGateway>true</sendToGateway>"
                                "<Observers><FrontEnd><AccountMgrDeskID><Id>-1</Id><enabled>false</enabled>"
                                "</AccountMgrDeskID></FrontEnd></Observers>"
                                "<AccountGroup><enabled>true</enabled><id>SBK</id></AccountGroup></TradeCapture>")
        quod = tree.getroot().find("ors")
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(60)

        # endregion
        # region step 1: Send 35 = D message
        self.fix_message.change_parameters({"Account": self.account})
        responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = responses[0].get_parameters()['OrderID']
        party = {'NoPartyIDs': [
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4')
        ]}
        list_ignored_fields = ['GatingRuleCondName', 'GatingRuleName', 'Account', 'PartyRoleQualifier',
                               'ReplyReceivedTime', 'SettlCurrency', 'LastExecutionPolicy',
                               'SecondaryOrderID', 'Text', 'VenueType', 'SecondaryExecID', "Text", 'LastMkt',
                               'TradePublishIndicator','PtysSubGrp']
        self.exec_report.change_parameters(
            {"Parties": party})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report,
                                                         ignored_fields=list_ignored_fields)
        party['NoPartyIDs'].remove(self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4'))
        party['NoPartyIDs'].remove(self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'))
        # endregion

        # region step 2: Manual Execute CO orders
        self.manual_execute.set_default_trade(exec_price=self.price, ord_id=order_id)
        self.manual_execute.update_fields_in_component('TradeEntryRequestBlock',
                                                       {'ReportVenueID': "PARIS",
                                                        'TradePublishIndicator': 'PTR',
                                                        'TargetAPA': "LUK",
                                                        'AssistedReportAPA': "NAS",
                                                        'OnExchangeRequested': "ONR",
                                                        'CounterpartList': {'CounterpartBlock':
                                                            [
                                                                self.data_set.get_counterpart_id_java_api(
                                                                    'counterpart_executing_firm'),
                                                                self.data_set.get_counterpart_id_java_api(
                                                                    'counterpart_contra_firm')]

                                                        }})
        party['NoPartyIDs'].extend([self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
                                    self.data_set.get_counterpart_id_fix('counter_part_id_executing_firm'),
                                    self.data_set.get_counterpart_id_fix('counterpart_java_api_user'),
                                    self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user')])
        self.java_api_manager.send_message_and_receive_response(self.manual_execute)
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {"Parties": party})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_ignored_fields)
        exec_id = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        # endregion

        # region step 3: Cancel execution of CO order
        self.manual_execute.get_parameters().clear()
        self.manual_execute.set_default_cancel_execution(order_id, exec_id)
        self.java_api_manager.send_message_and_receive_response(self.manual_execute)
        self.exec_report.set_default_trade_cancel(self.fix_message)
        self.exec_report.change_parameters(
            {"Parties": party})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_ignored_fields)
        # endregion

        # region step 3 part 2: Verify Gateway_TradingReport message
        value = self._get_logs_from_ors()
        list_of_needed_counterparts = [self.data_set.get_party_role('party_role_contra_firm'),
                                       self.data_set.get_party_role('party_role_executing_firm')]
        actually_results = True
        print(value)
        for counterpart in list_of_needed_counterparts:
            if value.find(f'PartyRole={counterpart}') == -1:
                actually_results = False
                break
        self.java_api_manager.compare_values({'CounterpartPresent': True},
                                             {'CounterpartPresent': actually_results},
                                             'Verify that TradeCaptureReport has ContraFirm and Executing Firm '
                                             'counterpart (step 3)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        os.remove("temp.xml")
        self.ssh_client.close()

    def _get_logs_from_ors(self):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "serializing gateway TradeCaptureReport" QUOD.ORS.log > logs.txt')
        self.ssh_client.get_file('/Logs/quod317/logs.txt', './logs.txt')
        file = open('./logs.txt')
        values = []
        for row in file:
            values.append(deepcopy(row))
        file.close()
        os.remove('./logs.txt')
        return values[-1]
