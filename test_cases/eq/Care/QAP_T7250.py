import logging
import os
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.ors_messages.AssignInstrumentRequest import AssignInstrumentRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7250(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity_2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager_2 = JavaApiManager(self.java_api_connectivity_2, self.test_id)
        self.new_order = FixNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2_ext_id")
        self.accept_request = CDOrdAckBatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path_cs = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path_cs = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.assign_instrument = AssignInstrumentRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.new_order.set_default_care_limit()
        dummy_instrument = self.data_set.get_java_api_instrument('instrument_dummy')
        self.new_order.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ClientAccountGroupID.value: self.client,
            JavaApiFields.InstrumentBlock.value: dummy_instrument
        })
        self.java_api_manager_2.send_message_and_receive_response(self.new_order)
        order_notification = \
            self.java_api_manager_2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.SecurityID.value: dummy_instrument[JavaApiFields.SecurityID.value],
             JavaApiFields.InstrSymbol.value: dummy_instrument[JavaApiFields.InstrSymbol.value],
             JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_notification, 'Verifying that order created (step 1)')
        order_id = order_notification[JavaApiFields.OrdID.value]
        # endregion

        # region step 2: Verify that ORS does not send "Internal_PositionCalcRequest" for Dummy Instrument
        self.java_api_manager.compare_values(
            {'Internal_PositionCalcRequestIsPresent': self._get_logs_from_ors(order_id)},
            {'Internal_PositionCalcRequestIsPresent': 'false'},
            'Verify that Internal_PositionCalcRequest does not present (step 2)')
        # endregion

        # region step 3: Accept CO order:
        cd_ord_notif_message = self.java_api_manager_2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, order_reply,
            f'Verifying that order created (step 3)')
        # endregion

        # region step 4-5: Set correct instrument
        listing_id = self.data_set.get_listing_id_by_name("listing_1")
        instr_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.assign_instrument.set_default([listing_id], instr_id, order_id)
        self.java_api_manager.send_message_and_receive_response(self.assign_instrument)
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrdNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.InstrID.value: instr_id},
                                             order_notification, 'Verify that user has correct instrument (step 5)')
        # endregion

        # region step 6: Verify that ORS sent Internal_PositionCalcRequest
        self.java_api_manager.compare_values(
            {'Internal_PositionCalcRequestIsPresent': self._get_logs_from_ors(order_id)},
            {'Internal_PositionCalcRequestIsPresent': 'true'},
            'Verify that Internal_PositionCalcRequest presents (step 6)')
        # endregion

    def _get_logs_from_ors(self, order_id):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command(
            f'egrep "serializing internal PositionCalcRequest.*{order_id}" QUOD.ORS.log > logs.txt')
        self.ssh_client.get_file('/Logs/quod317/logs.txt', './logs.txt')
        file = open('./logs.txt')
        values = file.readlines()
        file.close()
        os.remove('./logs.txt')
        if len(values) == 0:
            return 'false'
        else:
            return 'true'
