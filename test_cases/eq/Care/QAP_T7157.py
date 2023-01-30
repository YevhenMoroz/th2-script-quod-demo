import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7157(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.account_new = self.data_set.get_account_by_name('client_pt_1_acc_2')
        self.venue_client_account_first = self.data_set.get_venue_client_account(
            'client_pt_1_acc_1_venue_client_account')
        self.venue_client_account_second = self.data_set.get_venue_client_account(
            'client_pt_1_acc_2_venue_client_account')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.modify_request = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'AccountGroupID': self.client, 'PreTradeAllocationBlock': {
                                                         'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                             {'AllocAccountID': self.account,
                                                              'AllocQty': '100'}]}}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        # endregion

        # region verify values
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        order_id = ord_reply_block['OrdID']
        self.java_api_manager.compare_values({JavaApiFields.SingleAllocAccountID.value: self.account,
                                              JavaApiFields.VenueClientAccountName.value: self.venue_client_account_first,
                                              JavaApiFields.ExecType.value: OrderReplyConst.TransStatus_OPN.value},
                                             ord_reply_block,
                                             'Check order\'s VenueClientAccountName and SingleAllocAccountID')
        # endregion

        # region amend order
        self.modify_request.set_default(self.data_set, order_id)
        self.modify_request.update_fields_in_component('OrderModificationRequestBlock',
                                                       {'AccountGroupID': self.client, 'PreTradeAllocationBlock': {
                                                           'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                                                               {'AllocAccountID': self.account_new,
                                                                'AllocQty': '100'}]}}})
        self.java_api_manager.send_message_and_receive_response(self.modify_request)
        # endregion

        # region extract Venue Client Account
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.SingleAllocAccountID.value: self.account_new,
                                              JavaApiFields.VenueClientAccountName.value: self.venue_client_account_second,
                                              JavaApiFields.ExecType.value: OrderReplyConst.ExecType_REP.value},
                                             ord_reply_block,
                                             'Check order\'s VenueClientAccountName and SingleAllocAccountID after amending')
        # endregion
