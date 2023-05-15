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
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderModificationRequestOMS import \
    FixOrderModificationRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7145(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.new_order = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_modification_request = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2")
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.accept_request = CDOrdAckBatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.rule_manager = RuleManager(Simulators.equity)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_cancel_reject = FixMessageOrderCancelRejectReportOMS()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree = ET.parse(self.local_path)
        cs = tree.getroot().find("cs/fixAutoAcknowledge")
        cs.text = 'false'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        time.sleep(80)
        # endergion

        # region  step 1: create CO order via FIX
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.new_order.set_default_care_limit(account='client_2')
        price = self.new_order.get_parameters()[JavaApiFields.Price.value]
        self.new_order.add_tag({'header': {
            JavaApiFields.SenderSubID.value: 'SENDER_SUB_ID',
            JavaApiFields.TargetSubID.value: 'TARGET_SUB_ID',
            JavaApiFields.DeliverToCompID.value: 'DELIVER_TO_COMP_ID',
            JavaApiFields.DeliverToSubID.value: 'DELIVER_TO_SUB_ID',
            JavaApiFields.OnBehalfOfCompID.value: 'ON_BEHALF_OF_COMP_ID',
            JavaApiFields.OnBehalfOfSubID.value: 'ON_BEHALF_OF_SUB_ID'
        }})
        self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order)
        execution_report_last = self.fix_manager.get_last_message('ExecutionReport').get_parameters()
        parent_order_id = execution_report_last['OrderID']
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(f"SELECT cdordnotifid FROM cdordnotif WHERE transid = '{parent_order_id}'")[
                0][0]))
        self.accept_request.set_default(parent_order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
            f'Verifying that order created (step 1)')

        # endregion

        # region step 2:
        self.order_modification_request.set_default(self.new_order)
        self.fix_manager.send_message(self.order_modification_request)
        # endreigon

        # region reject modify request:step 2-3
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(
                f"SELECT cdordnotifid FROM cdordnotif WHERE transid = '{parent_order_id}' AND cdrequesttype='MOD'")[
                0][0]))
        self.accept_request.set_default(parent_order_id, cd_ord_notif_id, desk, 'M', set_reject=True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.Price.value: str(float(price))}, order_reply,
            f'Verifying that order is not changed (step 3)')
        # endregion

        # region step 4:
        list_ignore_field = ['CxlRejResponseTo', 'Account',
                             'Text', 'MsgType', 'MsgSeqNum',
                             'TargetCompID', 'SenderCompID', 'BeginString',
                             'BodyLength', 'ApplVerID', 'SendingTime']
        self.order_cancel_reject.set_default(self.new_order)
        self.order_cancel_reject.change_parameters({'header': {
            JavaApiFields.SenderSubID.value: 'TARGET_SUB_ID',
            JavaApiFields.TargetSubID.value: 'SENDER_SUB_ID',
            JavaApiFields.DeliverToCompID.value: 'ON_BEHALF_OF_COMP_ID',
            JavaApiFields.DeliverToSubID.value: 'ON_BEHALF_OF_SUB_ID',
            JavaApiFields.OnBehalfOfCompID.value: 'DELIVER_TO_COMP_ID',
            JavaApiFields.OnBehalfOfSubID.value: 'DELIVER_TO_SUB_ID',
        }})
        self.fix_verifier.check_fix_message_fix_standard(self.order_cancel_reject, ignored_fields=list_ignore_field,
                                                         ignore_header=False)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart CS")
        os.remove('temp.xml')
        time.sleep(80)
        self.ssh_client.close()
