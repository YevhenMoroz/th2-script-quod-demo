import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7019(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.str_name = 'Urgency'
        self.ex_str_name = '14'
        self.params = {
            "TargetStrategy": "1021",
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': "ExternalStrategyName",
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare CS configuration
        tree = ET.parse(self.local_path)
        cs = tree.getroot().find("cs/autoAcknowledge")
        cs.text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        time.sleep(80)
        # endregion

        # region step 1: Create CO order without algo param and check 35=8 message
        # part 1: Create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # end_of_part

        # part 2: Check 35=8
        ignored_fields = ['GatingRuleCondName', 'GatingRuleName']
        execution_report_1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(execution_report_1, ignored_fields=ignored_fields)
        time.sleep(10)
        # end_of_part
        # endregion

        # region step 2: Send FixOrderCancelReplaceRequest and check 35=8 message

        # part 1: Send FixMessageOrderCancelReplaceRequest
        fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(self.fix_message)
        fix_message_cancel_replace.add_tag(self.params)
        self.fix_manager.send_message_and_receive_response_fix_standard(fix_message_cancel_replace)
        # end_of_part

        # part 2: Check FixExecutionReport
        execution_report_2 = FixMessageExecutionReportOMS(self.data_set).set_default_replaced(self.fix_message)
        execution_report_2.add_tag(self.params)
        execution_report_2.change_parameters({"OrigClOrdID": "*", "SettlDate": "*", "SettlType": "B"})
        self.fix_verifier.check_fix_message_fix_standard(execution_report_2, ignored_fields=ignored_fields)
        # end_of_part
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart CS")
        os.remove('temp.xml')
        time.sleep(80)
        self.ssh_client.close()
