import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, PKSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9154(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.ja_manager_second = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                                self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.accept_request = CDOrdAckBatchRequest()
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.request_for_position = RequestForPositions()
        self.listing_id = self.data_set.get_listing_id_by_name('listing_2')
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:  Set Client Commission and Agent Fees via WebAdmin
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        fee_type = self.data_set.get_misc_fee_type_by_name('stamp')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile,
                                                                         client=self.client)
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee_type=fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion
        # region step 1: Create CO order
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {
            "InstrID": self.instrument_id,
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            "AccountGroupID": self.client,
            "ClOrdID": bca.client_orderid(9)})
        self.ja_manager_second.send_message_and_receive_response(self.order_submit)
        cd_ord_notif = self.ja_manager_second.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif[JavaApiFields.CDOrdNotifID.value]
        order_id = cd_ord_notif[JavaApiFields.OrdID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, self.desk)
        self.ja_manager.send_message_and_receive_response(self.accept_request)
        # endregion
        # region step 2: Execute order
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {
            'LastMkt': self.data_set.get_mic_by_name("mic_2")
        })
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        result_for_washbook = self._extract_cum_values_for_washbook(self.washbook_acc)
        exp_res = {"DailyClientCommission": "0.0", "DailyFeeAmt": "0.0"}
        self.ja_manager.compare_values(exp_res, result_for_washbook, "Check Daily comm/fee",
                                       VerificationMethod.NOT_EQUALS)
        # endregion
        # region step 3: execute DB query and restart PKS
        self.ssh_client.send_command("sql")
        self.ssh_client.send_command('BEGIN;SELECT eod_posit_pks();FETCH ALL IN "<unnamed portal 1>";COMMIT;')
        self.ssh_client.send_command("exit")
        self.ssh_client.send_command("qrestart AQS PKS")
        result_for_washbook = self._extract_cum_values_for_washbook(self.washbook_acc)
        self.ja_manager.compare_values(exp_res, result_for_washbook, "Check Daily comm/fee")
        # endregion

    def _extract_cum_values_for_washbook(self, washbook):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              washbook)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
