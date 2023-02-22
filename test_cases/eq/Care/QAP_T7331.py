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
from test_framework.fix_wrappers.FixVerifier import FixVerifier
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
class QAP_T7331(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.price = '300'
        self.qty = '5000'
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.new_order = FixNewOrderSingleOMS(self.data_set)
        self.order_modification_request = FixOrderModificationRequestOMS(self.data_set)
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
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)

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
        # region precondition - step 1: create CO order via FIX
        desk = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.new_order.set_default_care_limit()
        parent_cl_ord_id = self.new_order.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.ClOrdID.value]
        self.new_order.update_fields_in_component('NewOrderSingleBlock',
                                                  {"Price": self.price,
                                                   "OrdQty": self.qty,
                                                   'ClientAccountGroupID': self.client})
        self.java_api_manager2.send_message_and_receive_response(self.new_order)
        cd_ord_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        parent_order_id = cd_ord_notif_message[JavaApiFields.OrdID.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(parent_order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        # endregion

        # region step 2: split CO order on Child CO order
        listing = self.data_set.get_listing_id_by_name("listing_3")
        instrument = self.data_set.get_instrument_id_by_name("instrument_2")
        child_co_qty = str(float(self.qty) / 2)
        self.order_submit.set_default_child_care(desk=desk, parent_id=parent_order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         "Price": self.price,
                                                         "OrdQty": child_co_qty,
                                                         'InstrID': instrument,
                                                         'AccountGroupID': self.client,
                                                         'ListingList': {'ListingBlock':
                                                             [{
                                                                 'ListingID': listing}]}
                                                     })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        cd_ord_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        child_co_order_id_second_level = cd_ord_notif_message[JavaApiFields.OrdID.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        # endregion

        # region step 3: split CO order to Child DMA order
        self.order_submit.get_parameters().clear()
        nos_rule = child_ord_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names, self.venue,
                int(self.price))
            self.order_submit.set_default_child_dma(parent_order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'Price': self.price,
                                                                                 'InstrID': instrument,
                                                                                 "OrdQty": child_co_qty,
                                                                                 'AccountGroupID': self.client,
                                                                                 'ExecutionPolicy': 'DMA'})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_ord_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                f'Verifying that Child DMA {child_ord_id} (2 level)created (step 3)')
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 4-5 : Accept Child CO order
        self.accept_request.set_default(child_co_order_id_second_level, cd_ord_notif_id, desk)
        self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager2.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                              order_reply,
                                              f'Verifying that {child_co_order_id_second_level} is open (step 5)')
        # endergion

        # region step 6: Split Child CO order to DMA order
        child_ord_id_third_level = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names, self.venue,
                int(self.price))
            self.order_submit.set_default_child_dma(child_co_order_id_second_level)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'Price': self.price,
                                                                                 'InstrID': instrument,
                                                                                 "OrdQty": child_co_qty,
                                                                                 'AccountGroupID': self.client,
                                                                                 'ExecutionPolicy': 'DMA'})
            self.java_api_manager2.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_ord_id_third_level = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager2.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
                f'Verifying that Child DMA {child_ord_id_third_level} (3 level) created (step 6)')
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 7-8: Send Order Modification Request on parent order
        modify_price = str(float('150'))
        self.order_modification_request.set_modify_order_limit(parent_cl_ord_id, self.qty, modify_price)
        self.order_modification_request.update_fields_in_component('OrderModificationRequestBlock',
                                                                   {'ClientAccountGroupID': self.client})
        self.java_api_manager2.send_message_and_receive_response(self.order_modification_request)
        # endregion

        # region step 9: Accept Modify + Child
        modification_rule = None
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            True)
            cd_ord_notif_message = \
                self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
                    [JavaApiFields.CDOrdNotifBlock.value]
            cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
            self.accept_request.get_parameters().clear()
            self.accept_request.set_default(parent_order_id, cd_ord_notif_id, desk, 'M')
            self.accept_request.update_fields_in_component('CDOrdAckBatchRequestBlock', {'ModifyChildren': 'Y'})
            self.java_api_manager.send_message_and_receive_response(self.accept_request,
                                                                    {parent_order_id: parent_order_id,
                                                                     child_ord_id: child_ord_id})

            order_reply_parent = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, parent_order_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecType_PMO.value},
                                                 order_reply_parent,
                                                 f'Verify that parent order {parent_order_id} has PMO status (step 9)')
            order_reply_child_dma = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, child_ord_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.Price.value: str(float(modify_price))},
                                                 order_reply_child_dma,
                                                 f'Verify that child DMA order {child_ord_id} has  new price (step 9)')
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(modification_rule)
        # endregion

        # region step 10-11: Accept child modification_reqeust
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            True)
            cd_ord_notif_message = \
                self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
                    [JavaApiFields.CDOrdNotifBlock.value]
            cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
            self.accept_request.get_parameters().clear()
            self.accept_request.set_default(child_co_order_id_second_level, cd_ord_notif_id, desk, 'M')
            self.accept_request.update_fields_in_component('CDOrdAckBatchRequestBlock', {'ModifyChildren': 'Y'})
            self.java_api_manager2.send_message_and_receive_response(self.accept_request,
                                                                     {parent_order_id: parent_order_id,
                                                                      child_co_order_id_second_level: child_co_order_id_second_level,
                                                                      child_ord_id_third_level: child_ord_id_third_level})
            order_reply_parent = \
                self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value,
                                                        parent_order_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager2.compare_values({JavaApiFields.Price.value: modify_price},
                                                  order_reply_parent,
                                                  f'Verify that parent order {parent_order_id} has new price (step 11)')
            order_reply_child_co_order = \
                self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value,
                                                        child_co_order_id_second_level).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager2.compare_values({JavaApiFields.Price.value: modify_price},
                                                  order_reply_child_co_order,
                                                  f'Verify that child CO order {child_co_order_id_second_level} has  new price (step 11)')

            order_reply_child_dma_order_third_level = \
                self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value,
                                                        child_ord_id_third_level).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager2.compare_values({JavaApiFields.Price.value: modify_price},
                                                  order_reply_child_dma_order_third_level,
                                                  f'Verify that child DMA order third level {child_ord_id_third_level} has  new price (step 11)')
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(modification_rule)
        # endregion

        # region step 13: Check that 35=G messages sends to buy_gateway:
        # part 1: Check 35=G message for first child DMA order (second level of parent order)
        list_ignored_fields = [
            'Account', 'OrderQtyData', 'OrdType', 'ClOrdID', 'OrderCapacity', 'OrderID',
            'TransactTime', 'Side', 'Parties', 'Price', 'SettlCurrency', 'Currency',
            'TimeInForce', 'PositionEffect','Instrument','HandlInst','ExDestination']
        order_modification_request_fix = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        order_modification_request_fix.change_parameters({
            "OrigClOrdID": child_ord_id
        })
        self.fix_verifier.check_fix_message_fix_standard(order_modification_request_fix, ignored_fields=list_ignored_fields)
        # end_of_part

        # part 2: Check 35=G message for second child DMA order (third level of parent order)
        order_modification_request_fix.change_parameters({
            "OrigClOrdID": child_ord_id_third_level
        })
        self.fix_verifier.check_fix_message_fix_standard(order_modification_request_fix, ignored_fields=list_ignored_fields)
        # end_of_part

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart CS")
        os.remove('temp.xml')
        time.sleep(80)
        self.ssh_client.close()
