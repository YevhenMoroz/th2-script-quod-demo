import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, TimeInForces
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7334(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.price = '20'
        self.new_stop_price = '19'
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_modification_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2")
        self.accept_request = CDOrdAckBatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_cs = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path_cs = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition part 1: set needed configuration:
        tree_cs = ET.parse(self.local_path_cs)
        cs = tree_cs.getroot().find("cs/fixAutoAcknowledge")
        cs.text = 'false'
        tree_cs.write("temp_cs.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path_cs, "temp_cs.xml")
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(40)
        # endregion

        # region precondition: create CO order via FIX
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.new_order.set_default_care_limit(account='client_2')
        cl_ord_id = self.new_order.get_parameters()['ClOrdID']
        self.new_order.change_parameters({
            "TimeInForce": '1',
            'StopPx': self.price,
            'Price': self.price,
            'OrdType': '4',
        })
        self.fix_manager.send_message_fix_standard(self.new_order)
        time.sleep(2)
        order_id = self.db_manager.execute_query(f"SELECT ordid FROM ordr WHERE clordid = '{cl_ord_id}'")[
            0][0]
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(f"SELECT cdordnotifid FROM cdordnotif WHERE transid = '{order_id}'")[
                0][0]))
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
            f'Verifying that order created (precondition)')
        # endregion

        # region step 1: send 35=G message and accept its
        self.order_modification_request.set_default(self.new_order)
        self.order_modification_request.change_parameters({
            "TimeInForce": '0',
            "StopPx": self.new_stop_price
        })
        self.fix_manager.send_message(self.order_modification_request)
        time.sleep(2)
        # endregion

        # region step 2-3: Accept modification for CO order
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(f"SELECT cdordnotifid FROM cdordnotif WHERE transid = '{order_id}' AND "
                                          f"cdrequesttype = 'MOD'")[0][0]))
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, 'M', set_reject=True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.StopPrice.value: str(float(self.price)),
             JavaApiFields.TimeInForce.value: TimeInForces.GTC.value}, order_reply,
            f'Verifying that StopPrice and TIF does not change (step 3)')
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path_cs, self.local_path_cs)
        self.ssh_client.send_command("qrestart QUOD.CS")
        os.remove('temp_cs.xml')
        time.sleep(50)
        self.ssh_client.close()
