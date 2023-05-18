import logging
import time
from pathlib import Path
import os
from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst

from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T9036(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.commission_profile_vat = self.data_set.get_comm_profile_by_name('perc_qty')
        self.fee_type_vat = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        self.fee_charge_type = self.data_set.get_misc_fee_type_by_name('charges')
        self.venue = self.data_set.get_venue_by_name('venue_1')
        self.curr = self.data_set.get_currency_by_name('currency_1')
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        tree.getroot().find("execVATCommissionsEnable").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS CS")
        time.sleep(60)

        # region set client_commission precondition
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee_type=self.fee_type_vat,
                                                            comm_profile=self.commission_profile_vat).change_message_params(
            {'venueID': self.venue, 'miscFeeCategory': self.fee_charge_type})
        self.rest_commission_sender.send_post_request()

        # endregion

        # region create Care  orders (step 1)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region manual execute Care order (step 2)
        self.trade_entry.set_default_trade(order_id, exec_price='20')
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        # endregion

        # region check VAT in the execution
        expected_fee = {JavaApiFields.MiscFeeType.value: 'VAT', JavaApiFields.MiscFeeAmt.value: '200.0',
                        JavaApiFields.MiscFeeCurr.value: self.curr, JavaApiFields.MiscFeeBasis.value: 'P',
                        JavaApiFields.MiscFeeRate.value: '10.0', JavaApiFields.MiscFeeCategory.value: 'CHA', }
        exec_fee = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)[JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0]
        self.java_api_manager.compare_values(expected_fee, exec_fee, 'Check VAT fee in the execution')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS CS")
        time.sleep(60)
        os.remove("temp.xml")
