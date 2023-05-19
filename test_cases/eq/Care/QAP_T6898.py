import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.ors_messages.AssignInstrumentRequest import AssignInstrumentRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableSecurityBlock import RestApiDisableSecurityBlock

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6898(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.rest_api_conn = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order = FixNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.accept_request = CDOrdAckBatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.disable_listing_request = RestApiDisableSecurityBlock(self.data_set)
        self.rest_api_manager = RestApiManager(self.rest_api_conn, self.test_id)
        self.assign_instrument = AssignInstrumentRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO order
        self.new_order.set_default_care_limit()
        dummy_instrument = self.data_set.get_java_api_instrument('instrument_dummy')
        self.new_order.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ClientAccountGroupID.value: self.client,
            JavaApiFields.InstrumentBlock.value: dummy_instrument
        })
        self.java_api_manager.send_message_and_receive_response(self.new_order)
        order_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.SecurityID.value: dummy_instrument[JavaApiFields.SecurityID.value],
             JavaApiFields.InstrSymbol.value: dummy_instrument[JavaApiFields.InstrSymbol.value]},
            order_notification, 'Verifying that order dummy (step 1)')
        order_id = order_notification[JavaApiFields.OrdID.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order is Open (step 1)')
        # endregion

        # region step 2-4: Disable Listing via WebAdmin
        self.disable_listing_request.set_default()
        self.rest_api_manager.send_post_request(self.disable_listing_request)
        time.sleep(2)
        # endregion

        # region step 5 :
        listing_id = self.data_set.get_listing_id_by_name("listing_10")
        instr_id = self.data_set.get_instrument_id_by_name("instrument_9")
        self.assign_instrument.set_default([listing_id], instr_id, order_id)
        self.java_api_manager.send_message_and_receive_response(self.assign_instrument)
        # endregion

        # region step 6
        listing_id = self.data_set.get_listing_id_by_name("listing_1")
        instr_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.assign_instrument.set_default([listing_id], instr_id, order_id)
        self.java_api_manager.send_message_and_receive_response(self.assign_instrument)
        order_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.InstrID.value: instr_id},
                                             order_notification, 'Verify that order has correct instrument (step 6)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.disable_listing_request.set_default_enable()
        self.rest_api_manager.send_post_request(self.disable_listing_request)
        time.sleep(2)

