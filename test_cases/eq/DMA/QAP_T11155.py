import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11155(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_modification_request = OrderModificationRequest()
        self.price = '3.0'
        self.colar_down = 4
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: set up needed configuration for listing
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_11_collar_eurex')
        listing_id = self.data_set.get_listing_id_by_name('listing_11_collar_eurex')
        self.db_manager.execute_query(f"""UPDATE listingdailyinfo SET  collarup=NULL, collardown={self.colar_down}
                                                  WHERE listingid = '{listing_id}'""")
        self.ssh_client.send_command("qrestart QUOD.AQS, QUOD.RDS, QUOD.ORS")
        time.sleep(80)
        # endregion

        # region Create DMA order : Step 1
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.InstrID.value: instrument_id,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_submit_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrderSubmitReply.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ErrorMsg.value: 'Order price is not within RD collar range.'}, order_submit_reply[JavaApiFields.MessageReply.value][
                JavaApiFields.MessageReplyBlock.value][0], 'Verifying error message (step 1)')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value}, order_submit_reply[JavaApiFields.NewOrderReplyBlock.value][
                JavaApiFields.Ord.value], 'Verifying that order is rejected (step 1)')

        # endregion
