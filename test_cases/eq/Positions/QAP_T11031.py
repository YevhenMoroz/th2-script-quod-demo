import logging
import os
import time
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    ExecutionReportConst, AllocationReportConst, ConfirmationReportConst, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T11031(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn,
                                         self.test_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_5')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.sec_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.trade_entry_oms = TradeEntryOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set up needed configuration
        self.db_manager.execute_query(f"DELETE FROM dailyposit WHERE accountid = '{self.washbook_acc}' AND  instrid = '{self.instrument_id}'")
        self.db_manager.execute_query(f"DELETE FROM posit WHERE accountid = '{self.washbook_acc}' AND instrid = '{self.instrument_id}'")
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("positions/maintainOnConfirmation").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST, QUOD.ORS QUOD.PKS")
        time.sleep(120)
        # endregion

        # region step 1: Create CO order:
        price = '10'
        qty = '100'
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.OrdQty.value: qty,
                                                      JavaApiFields.Price.value: price,
                                                      JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.WashBookAccountID.value: self.washbook_acc})
        self.ja_manager.send_message_and_receive_response(self.order_submit, response_time=15_000)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply, 'Verify that order created (step 1)')
        order_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region step 2: Manual execute CO order
        self.trade_entry_oms.set_default_trade(order_id, price, qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry_oms)
        execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verify that CO order fully filled (step 2)')
        # endregion

        # region step 3: Complete CO order
        self.complete_message.set_default_complete(order_id)
        self.ja_manager.send_message_and_receive_response(self.complete_message)
        order_reply = self.ja_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                           JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}
        self.ja_manager.compare_values(expected_result, order_reply, 'Verify that CO order completed ')
        # endregion

        # region step 4: Book CO order
        new_price = '20'
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value, {
            JavaApiFields.Qty.value: qty,
            JavaApiFields.AvgPx.value: new_price,
            JavaApiFields.AccountGroupID.value: self.client,
        })
        self.ja_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.ja_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                             JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
        }
        self.ja_manager.compare_values(expected_result, allocation_report, 'Verify that block created (step 4)')
        # endregion

        # region step 5-7: Approve and Allocate block
        self._extract_cum_values_for_acc(self.washbook_acc)
        self.approve_block.set_default_approve(alloc_id)
        self.ja_manager.send_message_and_receive_response(self.approve_block)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value, {
            JavaApiFields.AllocAccountID.value: self.sec_account,
            JavaApiFields.AllocQty.value: qty,
            JavaApiFields.AvgPx.value: new_price})
        self.ja_manager.send_message_and_receive_response(self.confirmation_request)
        # endregion

        # region step 8-9: Check DailyRealizedGrossPL and Today Fees
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.PositQty.value,
                                                                               self.washbook_acc]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        daily_gross_pl = str(float(qty) * float(price))
        self.ja_manager.compare_values({JavaApiFields.DailyRealizedGrossPL.value: daily_gross_pl},
                                       position_report,
                                       f'Verify that {JavaApiFields.TodayRealizedPL.value} was calculated properly (step 8-9)')
        # endregion

        # region step 10: Check Fix_PositionReport
        value = self._get_logs_from_pks()
        print(value)
        actually_results = True
        if value.find(f"PosAmtType=DailyRealizedGrossPL PosAmt={daily_gross_pl}") == -1:
            actually_results = False
        self.ja_manager.compare_values({'DailyRealizedGrossPL_Is_Present': True},
                                             {'DailyRealizedGrossPL_Is_Present': actually_results},
                                             'Verify that DailyRealizedGrossPL  is present (step 3)')
        # endregion

    def _extract_cum_values_for_acc(self, acc):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              acc)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST QUOD.ORS QUOD.PKS")
        time.sleep(120)
        os.remove("temp.xml")
        self.ssh_client.close()

    def _get_logs_from_pks(self):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "fix PositionReport.*.EquityWashBook" QUOD.PKS.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        file = open('./logs.txt')
        values = []
        for row in file:
            values.append(deepcopy(row))
        file.close()
        os.remove('./logs.txt')
        return values[0]
