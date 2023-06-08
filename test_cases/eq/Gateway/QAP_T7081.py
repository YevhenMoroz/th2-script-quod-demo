import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7081(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn,
                                         self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client = self.data_set.get_client_by_name('client_com_1')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.sec_account = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.order_submit = OrderSubmitOMS(data_set)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set up needed configuration
        client_list_first = self.data_set.get_cl_list_id('cl_list_comm_1')
        client_list_second = self.data_set.get_cl_list_id('cl_list_peq_4925')
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/FIXNotif/FIX/clientLists/clientList").text = str(client_list_first)
        quod.find("ors/FIXNotif/nonFIX/clientLists/clientList").text = str(client_list_first)
        quod.find("ors/AddFIXNotif/FIXNotif1/FIX/clientLists/clientList").text = str(client_list_second)
        quod.find("ors/AddFIXNotif/FIXNotif1/nonFIX/clientLists/clientList").text = str(client_list_second)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.ORS")
        time.sleep(45)
        # endregion

        # region step 1-2: Create and trade DMA order:
        self.order_submit.set_default_dma_limit()
        qty = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {
                                                         JavaApiFields.AccountGroupID.value: self.client
                                                     })
        new_order_single = trade_rule = order_id = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_name,
                                                                                            self.mic, float(price),
                                                                                            int(qty), 0)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value, OrderReplyConst.TransStatus_OPN.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            order_id = order_reply[JavaApiFields.OrdID.value]
            self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                           order_reply, f'Verify that order is open (step 1)')
            execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.ja_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report, 'Verifying that order is fully filled (step 2)')

        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 3: Create Block
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.AccountGroupID.value: self.client
                                                               })
        self.ja_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                             JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value}
        self.ja_manager.compare_values(expected_result, allocation_report,
                                       f'Verifying that Block {alloc_id} created properly (step 3)')
        ord_update = self.ja_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.ja_manager.compare_values({JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
                                        JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                                       ord_update,
                                       'Verifying that order has properly statuses after book (step 3)')
        # endregion

        # region step 4: Approve block
        self.approve_block.set_default_approve(alloc_id)
        self.ja_manager.send_message_and_receive_response(self.approve_block)
        allocation_report = self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                             JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value})
        self.ja_manager.compare_values(expected_result, allocation_report,
                                       'Verify that block has properly statuses after approve (step 4)')
        # endregion

        # region step 5: Allocate Block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value,
                                                             {
                                                                 JavaApiFields.AllocAccountID.value: self.sec_account
                                                             })
        self.ja_manager.send_message_and_receive_response(self.confirmation_request)
        allocation_report = self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                             JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
                                JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value})
        self.ja_manager.compare_values(expected_result, allocation_report,
                                       'Verify that block has properly statuses after approve (step 5)')
        expected_result.clear()
        expected_result.update({JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        confirmation_report = \
            self.ja_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.ja_manager.compare_values(expected_result, confirmation_report,
                                       'Verifying that allocation created and has properly statuses (step 5)')
        # endregion

        # region step 6: Verify that first backoffice gateway received 2 AllocationReports and 1 ConfirmationReport
        # part 1: Verify that ORS sends first AllocationReport  message to correct BO gateway and not present for
        template_first_alloc = f"serializing fix AllocationReport.*.OrdID=.{order_id}.*.AllocType=ReadyToBook.*"
        message_first_alloc = 'Verify that AllocationReport with AllocType = ReadyToBook was sent to correct ' \
                              'backoffice gateway (step 6)'
        template_for_finding_gateway_alloc = '.*.MessageType=.Fix_AllocationReport.*.QUOD.FIX_REPLY.gtwbo.*'
        self._verify_that_message_present(True, template_first_alloc, message_first_alloc,
                                          template_for_finding_gateway_alloc)
        # end_of_part

        # part 2: Verify that ORS sends first AllocationReport  message to correct BO gateway
        template_second_alloc = f"serializing fix AllocationReport.*.OrdID=.{order_id}.*.AllocType=Preliminary.*"
        message_second_alloc = 'Verify that AllocationReport with AllocType = Preliminary was sent to correct ' \
                               'backoffice gateway (step 6)'
        self._verify_that_message_present(True, template_second_alloc, message_second_alloc,
                                          template_for_finding_gateway_alloc)
        # end_of_part

        # part 3: Verify that ORS sends ConfirmationReport message to correct BO gateway
        template_conf = f"serializing fix Confirmation.*.OrdID=.{order_id}.*"
        message_confirmation = 'Verify that Confirmation with  was sent to correct ' \
                               'backoffice gateway (step 6)'
        template_for_finding_gateway_conf = '.*.MessageType=.Fix_Confirmation.*.QUOD.FIX_REPLY.gtwbo.*'
        self._verify_that_message_present(True, template_conf, message_confirmation, template_for_finding_gateway_conf)
        # end_of_part
        # endregion

        # region step 7: Verify that second backoffice gateway did not receive 2 AllocationReports and 1 ConfReport
        # part 1: Verify that ORS sends first AllocationReport  message to correct BO gateway and not present for
        message_first_alloc = message_first_alloc.replace('6', '7').replace('was sent to correct', 'was not sent to second')
        template_for_finding_gateway_alloc = template_for_finding_gateway_alloc.replace('QUOD.FIX_REPLY.gtwbo', 'DefaultORSLoginReplySubject')
        self._verify_that_message_present(False, template_first_alloc, message_first_alloc,
                                          template_for_finding_gateway_alloc)
        # end_of_part

        # part 2: Verify that ORS sends first AllocationReport  message to correct BO gateway
        message_second_alloc = message_second_alloc.replace('6', '7').replace('was sent to correct',
                                                                            'was not sent to second')
        self._verify_that_message_present(False, template_second_alloc, message_second_alloc,
                                          template_for_finding_gateway_alloc)
        # end_of_part

        # part 3: Verify that ORS sends ConfirmationReport message to correct BO gateway
        message_confirmation = message_confirmation.replace('6', '7').replace('was sent to correct',
                                                                            'was not sent to second')
        template_for_finding_gateway_conf = template_for_finding_gateway_conf.replace('QUOD.FIX_REPLY.gtwbo', 'DefaultORSLoginReplySubject')
        self._verify_that_message_present(False, template_conf, message_confirmation, template_for_finding_gateway_conf)
        # end_of_part
        # endregion

    def _get_logs_from_ors(self, template):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command(
            f'egrep "{template}" QUOD.ORS.log -A4 > logs.txt')
        self.ssh_client.get_file('/Logs/quod317/logs.txt', './logs.txt')
        with open('./logs.txt', 'r') as file:
            records = file.readlines()
            file.close()
            os.remove('./logs.txt')
        return records

    def _verify_that_message_present(self, expected_result, template, message, template_for_finding_gateway):
        records: list = self._get_logs_from_ors(template)
        list_result = re.findall(template_for_finding_gateway, str(records))
        result = True if len(list_result) != 0 else False
        self.ja_manager.compare_values({'IsReportPresent': expected_result},
                                       {'IsReportPresent': result},
                                       message)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.ORS")
        time.sleep(45)
        self.ssh_client.close()

