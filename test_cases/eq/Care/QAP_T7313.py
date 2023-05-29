import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, \
    ExecutionPolicyConst, CDResponsesConst, TimeInForces
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7313(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity_user_2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager_user_2 = JavaApiManager(self.java_api_connectivity_user_2, self.test_id)
        self.new_order = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_cancel_request = FixMessageOrderCancelRequestOMS()
        self.client = self.data_set.get_client_by_name("client_2")
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.accept_request = CDOrdAckBatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_cs = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path_cs = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.rule_manager = RuleManager(Simulators.equity)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree_cs = ET.parse(self.local_path_cs)
        tree_cs.getroot().find("cs/fixAutoAcknowledge").text = 'false'
        tree_cs.getroot().find("cs/fixAutoAckNewOrderEvenIfRecipientNotConnected").text = 'false'
        tree_cs.write("temp_cs.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path_cs, "temp_cs.xml")
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(50)
        # # endergion

        # region  precondition : create CO order via FIX
        qty = '3000'
        desk = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.new_order.set_default_care_limit(account='client_2')
        price = self.new_order.get_parameters()['Price']
        self.new_order.change_parameters({
            'OrderQtyData': {'OrderQty': qty},
        })
        self.fix_manager.send_message_fix_standard(self.new_order)
        time.sleep(2)
        cl_ord_id = self.new_order.get_parameters()['ClOrdID']
        order_id = self.db_manager.execute_query(f"SELECT ordid FROM ordr WHERE clordid = '{cl_ord_id}'")[0][0]
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(f"SELECT cdordnotifid FROM cdordnotif WHERE transid = '{order_id}'")[
                0][0]))
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
            f'Verifying that order created (step 1)')
        # endregion

        # region step 1-2: Create Child CO order
        self.order_submit.set_default_child_care(desk=desk, parent_id=order_id)
        listing_id = self.data_set.get_listing_id_by_name("listing_3")
        instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.OrdQty.value: qty,
            JavaApiFields.Price.value: price,
            JavaApiFields.TimeInForce.value: TimeInForces.GTC.value,
            JavaApiFields.InstrID.value: instr_id,
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]}
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                                    JavaApiFields.ParentOrdrList.value).get_parameters()[
            JavaApiFields.OrdNotificationBlock.value]
        child_co_order_id = order_notification[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             order_notification, 'Verify that order has Sts = Sent (step 2)')
        # endregion

        # region step 3-4: Accept Child CO order:
        cd_order_notif_message = \
            self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
                JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_order_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(child_co_order_id, cd_ord_notif_id, desk)
        self.java_api_manager_user_2.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager_user_2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that Child CO order is Open (step 4)')
        # endregion

        # region step 5: Split CO order
        child_dma_order_id = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names,
                self.venue,
                float(price))
            self.order_submit.set_default_child_dma(child_co_order_id)
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {
                                                             JavaApiFields.OrdQty.value: qty,
                                                             JavaApiFields.AccountGroupID.value: self.client,
                                                             JavaApiFields.Price.value: price,
                                                             JavaApiFields.InstrID.value: instr_id,
                                                             JavaApiFields.TimeInForce.value: TimeInForces.GTC.value,
                                                             JavaApiFields.ListingList.value: {
                                                                 JavaApiFields.ListingBlock.value: [
                                                                     {JavaApiFields.ListingID.value: listing_id}]}
                                                         })
            self.java_api_manager_user_2.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager_user_2.get_last_message(ORSMessageType.OrdReply.value,
                                                                        ExecutionPolicyConst.DMA.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_dma_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Verify that Child DMA order(3 level) is Open (step 5)')
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single)
        # endregion

        # region step 6-7: Send Order Cancel Request
        self.order_cancel_request.set_default(self.new_order)
        self.fix_manager.send_message_fix_standard(self.order_cancel_request)
        # endregion

        # region step 8: Accept + Cancel Child Request
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(
                f"SELECT cdordnotifid FROM cdordnotif WHERE transid ='{order_id}' AND cdrequesttype='{CDResponsesConst.CDRequestType_CAN.value}'")[
                0][0]))
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, ack_type='C')
        self.accept_request.update_fields_in_component(JavaApiFields.CDOrdAckBatchRequestBlock.value,
                                                       {
                                                           JavaApiFields.CancelChildren.value: 'Y'
                                                       })
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecType_PCA.value},
                                             order_reply,
                                             f'Verify that parent order has {JavaApiFields.ExecType.value} '
                                             f'equals {OrderReplyConst.ExecType_PCA.value}, (step 8)')
        # endregion

        # region step 9-10
        cd_order_notif_message = \
            self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
                JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_order_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(child_co_order_id, cd_ord_notif_id, desk, 'C', set_reject=True)
        self.java_api_manager_user_2.send_message_and_receive_response(self.accept_request)
        orders_id = [child_co_order_id, child_dma_order_id]
        for ord_id in orders_id:
            order = self.db_manager.execute_query(f"SELECT price FROM ordr WHERE ordid='{ord_id}'")
            self.java_api_manager.compare_values({JavaApiFields.Price.value: str(float(price))},
                                                 {JavaApiFields.Price.value: str(float(order[0][0]))},
                                                 f'Verify that {ord_id} does not change (step 10)')
        result = self.db_manager.execute_query(f"SELECT exectype FROM ordreply WHERE transid = '{order_id}' AND requestid !='{order_id}'")
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecType_PCA.value},
                                             {JavaApiFields.ExecType.value: result[0][-1]},
                                             f'Verify that order Parent Order has Sts = {OrderReplyConst.ExecType_PCA.value} (step 10)')
        self.java_api_manager.compare_values({'CheckThatRecordOnlyOne': 1},
                                             {'CheckThatRecordOnlyOne': len(result[0])},
                                             "Verify that OrderReply only one at DB (part of step 10)")
        # endregion

        # region step 11- 12: Reject CDOrdNotif message for Parent CO order
        time.sleep(2)
        cd_ord_notif_id = str(int(
            self.db_manager.execute_query(
                f"SELECT cdordnotifid FROM cdordnotif WHERE transid ='{order_id}' AND cdrequesttype='{CDResponsesConst.CDRequestType_CAN.value}'")[
                0][0]))
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk, ack_type='C', set_reject=True)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.Price.value: str(float(price))},
                                             order_reply,
                                             f'Verify that parent order does not change (step 12)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path_cs, self.local_path_cs)
        self.ssh_client.send_command("qrestart QUOD.CS")
        os.remove('temp_cs.xml')
        time.sleep(50)
        self.ssh_client.close()
        self.db_manager.close_connection()
