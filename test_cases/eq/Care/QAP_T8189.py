import logging
from custom import basic_custom_actions as bca, basic_custom_actions
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiVenueListMessages import RestApiVenueListMessages
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8189(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_list_request = RestApiVenueListMessages(self.data_set)
        self.venue = self.data_set.get_venue_id('paris')
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)
        self.client = self.data_set.get_client_by_name('client_1')
        self.venue_id = self.data_set.get_venue_list('test_auto')
        self.order_submit = OrderSubmitOMS(data_set)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.exec_policy = self.data_set.get_exec_policy('execution_policy_C')
        self.wash_book_acc = self.data_set.get_washbook_account_by_name('washbook_account_4')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up washbook rule on Client, Desk, Venue List QAP_T8188
        venue_list = [self.venue]
        self.venue_list_request.modify_venue_list(venue_list)
        self.rest_api_manager.send_post_request(self.venue_list_request)
        self.rest_wash_book_message.disable_care_wash_book_rule()
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        self.rest_wash_book_message.modify_wash_book_rule(venue_list_id=self.venue_id)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply_block,
                                             'Check WashBook Account for first case - Venue List')
        # endregion

        # region set up washbook rule on Client, Desk, Venue List QAP_T8189
        self.rest_wash_book_message.modify_wash_book_rule(client=self.client, venue_list_id=self.venue_id,
                                                          desk=self.desk)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.AccountGroupID.value: self.client},
                                             ord_reply_block,
                                             'Check WashBook Account for first case - Client, Desk, Venue List')
        # endregion

        # region set up washbook rule on Desk and Venue List QAP_T8190
        self.rest_wash_book_message.modify_wash_book_rule(desk=self.desk, venue_list_id=self.venue_id)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply_block,
                                             'Check WashBook Account for third case - Desk and Venue List')
        # endregion

        # region set up washbook rule on Execution Policy, Desk and Venue List QAP_T8191
        self.rest_wash_book_message.modify_wash_book_rule(desk=self.desk, venue_list_id=self.venue_id,
                                                          exec_policy=self.exec_policy)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.CARE.value},
                                             ord_reply_block,
                                             'Check WashBook Account for third case - Execution Policy, Desk and Venue List')
        # endregion

        # region set up washbook rule on Execution Policy, Venue List QAP_T8192
        self.rest_wash_book_message.modify_wash_book_rule(venue_list_id=self.venue_id,
                                                          exec_policy=self.exec_policy)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.CARE.value},
                                             ord_reply_block,
                                             'Check WashBook Account for third case - Execution Policy, Venue List')
        # endregion

        # region set up washbook rule on Execution Policy = Care, Client and Venue List QAP_T8193
        self.rest_wash_book_message.modify_wash_book_rule(client=self.client, venue_list_id=self.venue_id,
                                                          exec_policy=self.exec_policy)
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region create order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {"ClOrdID": basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # check wash book account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.WashBookAccountID.value: self.wash_book_acc,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.AccountGroupID.value: self.client,
                                              JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.CARE.value},
                                             ord_reply_block,
                                             'Check WashBook Account for second case - Execution Policy, Client, Venue List')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.venue_list_request.set_default_venue_list()
        self.rest_api_manager.send_post_request(self.venue_list_request)
        self.rest_wash_book_message.clear_washbook_rule()
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        self.rest_wash_book_message.enable_care_wash_book_rule()
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
