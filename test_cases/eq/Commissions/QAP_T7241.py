import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, OrderReplyConst, JavaApiFields, \
    ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7241(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '7241'
        self.price = '10'
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.complete_order_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        self.rest_commission_sender.clear_fees()
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        route_id = self.data_set.get_route_id_by_name('route_1')
        comm_order_scope = self.data_set.get_fee_order_scope_by_name('done_for_day')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile, fee=fee,
                                                            fee_type=agent_fee_type)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
            'routeID': route_id,
            'instrType': instr_type,
            'orderCommissionProfileID': commission_profile,
            'commOrderScope': comm_order_scope
        })
        self.rest_commission_sender.send_post_request()
        # endregion

        # region change value in DB (Precondition)
        self.ssh_client.send_command("~/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.ESBUYTH2TEST QUOD.CS")
        time.sleep(80)
        # endregion

        # region create CO order (step 1)
        self.order_submit.set_default_care_limit(recipient=self.data_set.get_recipient_by_name('recipient_user_1'),
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value).remove_fields_from_component(
            'NewOrderSingleBlock', ['SettlCurrency'])
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
            'RouteList': {'RouteBlock': [{'RouteID': route_id}]}
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create CO order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        status = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.TransStatus.value]
        self.order_book.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            f'Comparing {OrderBookColumns.sts.value}')
        # endregion

        # region trade CO order (step 2, step 3, step 4)
        counter_part = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'CounterpartList': {'CounterpartBlock': [counter_part]}})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        print_message('Trade CO order', responses)
        misc_fee_type = 'AGE'
        misc_fee_basis = 'P'
        misc_fee_basis_after_compute = 'A'
        misc_fee_curr = self.data_set.get_currency_by_name('currency_2')
        misc_fee_rate = '5.0'
        misc_fee_amount = str(float(self.price) * float(self.qty) / 10000 * float(misc_fee_rate))
        misc_fee_block_expected = {'MiscFeeType': misc_fee_type, 'MiscFeeBasis': misc_fee_basis,
                                   'MiscFeeAmt': misc_fee_amount, 'MiscFeeRate': misc_fee_rate,
                                   'MiscFeeCurr': misc_fee_curr}
        message = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters() \
            [JavaApiFields.ExecutionReportBlock.value]
        actually_result = message[JavaApiFields.TransExecStatus.value]
        exec_id = message[JavaApiFields.ExecID.value]
        misc_fee_block = message[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0]
        self.java_api_manager.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: actually_result},
            f'Comparing {OrderBookColumns.exec_sts.value}')
        self.java_api_manager.compare_values(misc_fee_block_expected, misc_fee_block,
                                             f'Comparing Fee of Execution {exec_id}')
        # endregion

        # region check miscFee in ComputeBookingMiscFeeCommissionsRequest (step 5)
        self.complete_order_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order_request)
        print_message('Complete message', responses)
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty)
        new_avg_px = str(int(self.price) / 100)
        self.compute_booking_fee_commission_request.update_fields_in_component(
            'ComputeBookingFeesCommissionsRequestBlock', {'AvgPx': new_avg_px, 'AccountGroupID': self.client})
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('Send ComputeBookingFeesCommissionsRequest', responses)
        misc_fee_amount_compute_reply = str(round(float(misc_fee_amount), 2))
        actual_result = \
            self.java_api_manager.get_last_message(
                ORSMessageType.Order_ComputeBookingFeesCommissionsReply.value).get_parameters()[
                JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][JavaApiFields.RootMiscFeesList.value][
                JavaApiFields.RootMiscFeesBlock.value][0]
        misc_fee_block_expected.clear()
        misc_fee_block_expected = {JavaApiFields.RootMiscFeeBasis.value: misc_fee_basis_after_compute,
                                   JavaApiFields.RootMiscFeeRate.value: misc_fee_amount_compute_reply,
                                   JavaApiFields.RootMiscFeeCurr.value: misc_fee_curr,
                                   JavaApiFields.RootMiscFeeType.value: misc_fee_type,
                                   JavaApiFields.RootMiscFeeAmt.value: misc_fee_amount_compute_reply}

        self.java_api_manager.compare_values(misc_fee_block_expected, actual_result,
                                             'Comparing Value after ComputeFeesCommissionRequest')
        # endregion

        # region create block
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        self.allocation_instruction_message.set_default_book(order_id)
        self.allocation_instruction_message.update_fields_in_component('AllocationInstructionBlock',
                                                                       {
                                                                           'GrossTradeAmt': gross_currency_amt,
                                                                           'AvgPx': self.price,
                                                                           'Qty': self.qty,
                                                                           'AccountGroupID': self.client,
                                                                           'Currency': misc_fee_curr,
                                                                           "InstrID": instrument_id,
                                                                           'RootCommissionDataBlock': {
                                                                               'RootCommission': misc_fee_amount_compute_reply,
                                                                               'RootCommType': 'A',
                                                                               'RootCommCurrency': misc_fee_curr
                                                                           },
                                                                           'RootMiscFeesList': {'RootMiscFeesBlock': [{
                                                                               JavaApiFields.RootMiscFeeType.value: 'AGE',
                                                                               JavaApiFields.RootMiscFeeAmt.value: misc_fee_amount_compute_reply,
                                                                               JavaApiFields.RootMiscFeeBasis.value: misc_fee_basis_after_compute,
                                                                               JavaApiFields.RootMiscFeeRate.value: misc_fee_amount_compute_reply,
                                                                               JavaApiFields.RootMiscFeeCurr.value: misc_fee_curr
                                                                           }]},
                                                                           'ExecAllocList': {
                                                                               'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                                   'ExecID': exec_id,
                                                                                                   'ExecPrice': new_avg_px}]},

                                                                       })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        print_message('Create Block', responses)
        actual_result = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()
        alloc_id = actual_result[JavaApiFields.AllocationReportBlock.value][JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(misc_fee_block_expected,
                                             actual_result[JavaApiFields.AllocationReportBlock.value][
                                                 JavaApiFields.RootMiscFeesList.value]
                                             [JavaApiFields.RootMiscFeesBlock.value][0],
                                             'Comparing value after Allocation Instruction')
        # endregion

        # region allocate block
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.alloc_account,
            'AllocQty': self.qty,
            'AvgPx': new_avg_px,
            "InstrID": instrument_id
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        actual_result = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        misc_fee_block_expected = {'MiscFeeType': misc_fee_type, 'MiscFeeBasis': misc_fee_basis_after_compute,
                                   'MiscFeeAmt': misc_fee_amount_compute_reply, 'MiscFeeRate': misc_fee_amount_compute_reply,
                                   'MiscFeeCurr': misc_fee_curr}
        self.java_api_manager.compare_values(misc_fee_block_expected, actual_result[JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0],
                                             'Comparing Fee after allocate')
        print_message('Allocate block', responses)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.send_command("~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.ESBUYTH2TEST QUOD.CS")
        time.sleep(80)


