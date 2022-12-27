import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET
from pkg_resources import resource_filename
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6899(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ss_connectivity = self.fix_env.sell_side
        self.api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.qty = '500'
        self.price = '20'
        self.alloc_account = 'test'
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rest_institution_message = RestApiModifyInstitutionMessage(self.data_set)
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
        self.rest_institution_message.modify_enable_unknown_accounts(False)
        self.api_manager.send_post_request(self.rest_institution_message)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/acceptFreeAllocAccountID").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(90)
        # endregion

        # region Create CO order via FIX and execute it
        no_allocs: dict = {'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty}]}
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, 'PreAllocGrp': no_allocs})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        txt = response[0].get_parameters()['Text']
        # endregion

        # check error in the exec report
        exp_text = '11642 Unknown account identifier: test / 11505 Runtime error (trying to get VSecurityAccount with an empty key)'
        self.java_api_manager.compare_values({'Text': exp_text}, {'Text': txt}, 'Check error in the exec report')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")