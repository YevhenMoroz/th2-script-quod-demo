import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
import xml.etree.ElementTree as ET
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7350(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.nin_wrong = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_2')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        # part 1: make changes for venue
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'Y'
                                            WHERE venueid = 'PARIS'""")
        tree = ET.parse(self.local_path)
        dma = tree.getroot().find("ors/FrontToBack/acceptUnknownAccountGroup/DMA")
        dma.text = 'false'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        # end_of_part
        self.ssh_client.send_command("qrestart all")
        time.sleep(140)
        # end_of_part

        # endregion:

        # region step 1-2: Create DMA order with wrong NIN (VenueClientAccountGroupName (VenueClientAccountName))
        self.new_order_single.set_default_dma_limit()
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.ClientAccountGroupID.value: self.nin_wrong})
        self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        ord_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value,
                                              JavaApiFields.FreeNotes.value: f"11620 unknown client {self.nin_wrong} / "
                                                                             f"11826 Waiting for Account Group determination "
                                                                             f"/ 11620 unknown client {self.nin_wrong}/ "
                                                                             f"11826 Waiting for Account Group determination / unknown client {self.nin_wrong}"},
                                             ord_notification,
                                             f'Verify that order rejected and has properly {JavaApiFields.FreeNotes.value}')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(f"""UPDATE  venue SET  valvenueclientaccountname  = 'N'
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.put_file(self.remote_path, self.local_path)
        os.remove("temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(140)
        self.db_manager.close_connection()
        self.ssh_client.close()
