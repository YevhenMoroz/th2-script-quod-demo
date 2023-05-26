import logging
import os
import time
from datetime import datetime
from pathlib import Path

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from pkg_resources import resource_filename
from xml.etree import ElementTree as ET
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10861(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_ors = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path_ors = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree_ors = ET.parse(self.local_path_ors)
        tree_ors.getroot().find("ors/benchmarking/benchmarks/DVW").text = 'true'
        tree_ors.write('temp_ors.xml')
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path_ors, 'temp_ors.xml')
        self.db_manager.execute_query("UPDATE venue SET timezone = 'Asia/Tokyo', opentime = '08:00:00',closetime='15:40:00' WHERE venueid ='PARIS'")
        self.ssh_client.send_command('qstart BS')
        self.ssh_client.send_command("qrestart all")
        time.sleep(140)
        # # endregion

        # region step 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply, "Verify that order created (step 1)")
        # endregion

        # region step 2
        start_date: str = (tm(datetime.utcnow().isoformat()) + bd(n=-1)).date().strftime('%Y-%m-%d') + 'T23:00'
        end_date: str = (tm(datetime.utcnow().isoformat())).date().strftime(
            '%Y-%m-%d') + 'T06:40'
        bench_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.BenchmarkNotification.value).get_parameters() \
                [JavaApiFields.BenchmarkNotificationBlock.value][JavaApiFields.BenchmarkList.value][
                JavaApiFields.BenchmarkBlock.value][0]
        self.java_api_manager.compare_values({JavaApiFields.StartBenchmarkTimestamp.value: start_date,
                                              JavaApiFields.EndBenchmarkTimestamp.value: end_date},
                                             bench_notification, 'Verify that benchmark has properly values (step 2)')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path_ors, self.local_path_ors)
        self.db_manager.execute_query(
            "UPDATE venue SET timezone = 'Europe/Paris', opentime = '01:00:00',closetime='00:00:00' WHERE venueid ='PARIS'")
        self.ssh_client.send_command("qrestart all")
        os.remove('temp_ors.xml')
        time.sleep(140)
        self.db_manager.close_connection()
        self.ssh_client.close()
