import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    OrderReplyConst, SubmitRequestConst, ConfirmationReportConst, AllocationInstructionConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyAccoutGroupMessage import RestApiModifyAccountGroupMessage
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T10350(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = '999'
        self.price = '99'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.client = self.data_set.get_client('client_rest_api')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rest_api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.mic = self.data_set.get_mic_by_name('mic_2')
        self.contra_firm = self.data_set.get_contra_firm('contra_firm_1')
        self.last_mkt = self.mic
        self.modify_account_group = RestApiModifyAccountGroupMessage(data_set, environment)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        # part 1: Set agent_fees
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        contra_firm = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        self.rest_commission_sender.clear_fees()
        all_exec_exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': all_exec_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # end_of_part

        # part 2: Set needed AccountGroup
        self.modify_account_group.set_default()
        self.rest_api_manager.send_post_request(self.modify_account_group)
        # end_of_part
        # endregion

        # region set up configuration on BackEnd(precondition)
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(120)
        # endregion

        # region step 1: Create CO order
        route_params = {JavaApiFields.RouteBlock.value: [
            {JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                       {
                                                           JavaApiFields.OrdCapacity.value: SubmitRequestConst.OrdCapacity_Agency.value,
                                                           JavaApiFields.OrdQty.value: self.qty,
                                                           JavaApiFields.AccountGroupID.value: self.client,
                                                           JavaApiFields.RouteList.value: route_params,
                                                           JavaApiFields.Price.value: self.price,
                                                           'ListingList': {'ListingBlock': [{'ListingID':
                                                               self.data_set.get_listing_id_by_name(
                                                                   "listing_2")}]},
                                                           JavaApiFields.InstrID.value: instrument_id
                                                           }
                                                       )
        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply_message[JavaApiFields.OrdID.value]
        actually_sts_field = order_reply_message[JavaApiFields.TransStatus.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             {JavaApiFields.TransStatus.value: actually_sts_field},
                                             'Comparing expected and actually results from step 1')
        # endregion

        # region step 2: Trade CO order with ContraFirm
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                    {JavaApiFields.CounterpartList.value: {
                                                        JavaApiFields.CounterpartBlock.value: [contra_firm]},
                                                     JavaApiFields.LastMkt.value: self.mic})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        actually_exec_sts = execution_report[JavaApiFields.TransExecStatus.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {JavaApiFields.TransExecStatus.value: actually_exec_sts},
            'Comparing expected and actually results from step 2')
        # endregion

        # region step 3:Check that execution has  Agent Fee
        misc_fee_rate = '5'
        execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0][
            JavaApiFields.MiscFeeAmt.value] = str(round(float(
            execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0][
                JavaApiFields.MiscFeeAmt.value]), 4))
        misc_fee_amount = float(misc_fee_rate) * float(self.qty) * float(self.price) / 10000
        self.java_api_manager.compare_values(
            {JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
             JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
             JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
             JavaApiFields.MiscFeeRate.value: str(float(misc_fee_rate)),
             JavaApiFields.MiscFeeAmt.value: str(misc_fee_amount)
             }, execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0],
            'Check that Agent fee presents in Execution Report (step 3)')
        # endregion

        # region step 4 : complete CO order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        actually_post_trade_status = order_reply_message[JavaApiFields.PostTradeStatus.value]
        actually_done_for_day = order_reply_message[JavaApiFields.DoneForDay.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            {JavaApiFields.PostTradeStatus.value: actually_post_trade_status,
             JavaApiFields.DoneForDay.value: actually_done_for_day},
            'Comparing expected and actually results (step 4)')
        # endregion

        # region step 5 : Check Booking
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]

        result = JavaApiFields.RootMiscFeesList.value in allocation_report
        self.java_api_manager.compare_values({'Result': False}, {'Result': result},
                                             'Check that Block doesn`t has Agent Fees (step 5)')
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report, 'Verify that block created and has properly statuses (step 5)')
        # endregion

        # region step 6 : Check Allocation
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        result = JavaApiFields.MiscFeesList.value in confirmation_report
        self.java_api_manager.compare_values({'Result': False}, {'Result': result},
                                             'Check that Confirmation doesn`t has Agent Fees (step 6)')
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value},
            confirmation_report, 'Verify that confirmation created and has properly statuses (step 6)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(120)
        self.ssh_client.close()
