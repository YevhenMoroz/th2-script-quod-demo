import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6900(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.price = '10'
        self.client = self.data_set.get_client('client_pt_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.ex_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.rest_institution_message = RestApiModifyInstitutionMessage(self.data_set)
        self.book_request = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.alloc_request = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.rest_institution_message.modify_enable_unknown_accounts(True)
        self.api_manager.send_post_request(self.rest_institution_message)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/acceptFreeAllocAccountID").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        # endregion

        # region create  DMA order via fix and trade it (step 1 and step 2)
        self.fix_message.set_default_dma_limit()
        alt_acount = 'AltAccount'
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        self.fix_message.add_tag({'PreAllocGrp': {'NoAllocs': [{'AllocAccount': alt_acount, 'AllocQty': self.qty}]}})
        trade_rule = False
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_name,
                                                                                            self.ex_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0
                                                                                            )
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            exex_rep = self.fix_manager.get_last_message("ExecutionReport", "M_PreAllocGrp").get_parameters()
            order_id = exex_rep["OrderID"]
            self.fix_manager.compare_values({"AllocAccount": alt_acount}, exex_rep['M_PreAllocGrp']['NoAllocs'][0],
                                            "Check Alloc Acc")
        except Exception as e:
            logger.error(f'{e}', exc_info=True)

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
            # endregion

            # region Step 5
            self.book_request.set_default_book(order_id)
            self.book_request.update_fields_in_component("AllocationInstructionBlock",
                                                         {"InstrID": self.data_set.get_instrument_id_by_name(
                                                             "instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.book_request)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                 JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
                allocation_report, 'Check booking')
            # endregion
            # region Step 6
            self.approve_request.set_default_approve(alloc_id)
            self.java_api_manager.send_message_and_receive_response(self.approve_request)
            expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                               JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                               JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
            self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
            # endregion
            # region Step 6
            self.alloc_request.set_default_allocation(alloc_id)
            self.alloc_request.update_fields_in_component("ConfirmationBlock", {"AllocFreeAccountID": alt_acount,
                                                                                "InstrID": self.data_set.get_instrument_id_by_name(
                                                                                    "instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.alloc_request)
            confirm_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            expected_result_confirmation = {
                JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
            actually_result = {
                JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
                JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value]}
            self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                                 f'Check statuses of confirmation of {alt_acount}')
            # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_institution_message.modify_enable_unknown_accounts(False)
        self.api_manager.send_post_request(self.rest_institution_message)
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        os.remove("temp.xml")
