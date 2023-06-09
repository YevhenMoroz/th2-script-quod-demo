import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, \
    ExecutionReportConst, CrossAnnouncementReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CrossAnnouncement import CrossAnnouncement
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11184(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.qty1 = '100'
        self.price1 = '5'
        self.qty2 = '120'
        self.price2 = '10'
        self.qty_to_execute = '20'
        self.qty_to_cross = '40'
        self.price_to_cross = '10'
        self.trade_request = TradeEntryOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.cross_announcement = CrossAnnouncement(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")  # CLIENT_COMM_1_EUREX
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create first Care order (precondition)
        listing_id = self.data_set.get_listing_id_by_name("listing_2")
        instr_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value
                                                   )
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdQty': self.qty1, "Price": self.price1, 'ListingList': {
                                                           'ListingBlock': [{
                                                               'ListingID': listing_id}]},
                                                        'InstrID': instr_id, 'AccountGroupID': self.client})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id1 = order_notif_message["OrdID"]
        # endregion

        # region create second Care order (precondition)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'Side': 'Sell', 'OrdQty': self.qty2, "Price": self.price2,
                                                        "ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id2 = order_notif_message["OrdID"]

        self.trade_request.set_default_trade(ord_id2, self.price2, self.qty_to_execute)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.CumQty.value: self.qty_to_execute + '.0'}, execution_report,
            'Check order after manual execution (Precondition)')
        # endregion

        # region step 1 : run script
        self.ssh_client.send_command("/home/quod317/specific_scripts/test_CrossAnnnouncement.sh")
        time.sleep(5)
        # endregion

        # region step 1-2 : Perform Market Cross action
        self.cross_announcement.set_default(ord_id1, ord_id2)
        self.cross_announcement.update_fields_in_component(JavaApiFields.CrossAnnouncementBlock.value,
                                                           {JavaApiFields.OrdQty.value: self.qty_to_cross,
                                                            JavaApiFields.Price.value: self.price_to_cross})
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(
                                                                                                      self.price_to_cross))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price_to_cross),
                                                                                            int(self.qty_to_cross), 2)
            self.java_api_manager.send_message_and_receive_response(self.cross_announcement, {ord_id1: ord_id1,
                                                                                              ord_id2: ord_id2},
                                                                    response_time=80000)
        finally:
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

        # region step 4: Check Child orders
        # Check first order
        order_notification_first = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id1).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdNotificationBlock.value: JavaApiFields.CrossAnnouncementID.value},
            order_notification_first, 'Check 1 child order contain CrossAnnouncementID (step 4)',
            VerificationMethod.CONTAINS)
        execution_report_first = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ord_id1).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report_first,
            'Check status of first child order after Cross Request (step 4)')

        # Check second order
        order_notification_second = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id1).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdNotificationBlock.value: JavaApiFields.CrossAnnouncementID.value},
            order_notification_second, 'Check 2 child order contain CrossAnnouncementID (step 4)',
            VerificationMethod.CONTAINS)
        execution_report_second = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ord_id2).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report_second,
            'Check status of second child order after Cross Request (step 4)')

        # Check CrossAnnouncementStatus in CrossAnnouncementReply
        cross_announs_reply = self.java_api_manager.get_last_message(
            ORSMessageType.CrossAnnouncementReply.value).get_parameter(
            JavaApiFields.CrossAnnouncementReplyBlock.value)
        self.java_api_manager.compare_values({
            JavaApiFields.CrossAnnouncementStatus.value: CrossAnnouncementReplyConst.CrossAnnouncementStatus_ACK.value},
            cross_announs_reply, 'Check status of CrossAnnouncement (step 4)')
        # endregion
