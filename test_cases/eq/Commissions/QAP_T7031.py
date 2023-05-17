import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, OrderReplyConst, JavaApiFields, \
    AllocTransTypes, AllocTypes
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


class QAP_T7031(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '2104'
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
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
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
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name('bas_qty'))
        self.rest_commission_sender.send_post_request()
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        commission_profile = self.data_set.get_comm_profile_by_name('bas_qty')
        fee = self.data_set.get_fee_by_name('fee_vat')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile, fee=fee,
                                                            fee_type=agent_fee_type)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
            'instrType': instr_type,
        })
        self.rest_commission_sender.send_post_request()
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

        # region trade CO order  and book it (step 2)
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        print_message('Trade CO order', responses)
        message = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters() \
            [JavaApiFields.ExecutionReportBlock.value]
        exec_id = message[JavaApiFields.ExecID.value]
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

        # region create block
        root_misc_fees = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.RootMiscFeesList.value]
        client_commission = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.ClientCommissionList.value]
        misc_fee_curr = root_misc_fees[JavaApiFields.RootMiscFeesBlock.value][0][JavaApiFields.RootMiscFeeCurr.value]
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        fee_amount = str(float(self.qty) * 0.5 * 0.02)
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
                                                                               'RootCommission': fee_amount,
                                                                               'RootCommType': 'A',
                                                                               'RootCommCurrency': misc_fee_curr
                                                                           },
                                                                           JavaApiFields.RootMiscFeesList.value: root_misc_fees,
                                                                           JavaApiFields.ClientCommissionList.value: client_commission,
                                                                           'ExecAllocList': {
                                                                               'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                                   'ExecID': exec_id,
                                                                                                   'ExecPrice': self.price}]},

                                                                       })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        print_message('Create Block', responses)
        actual_result = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                               JavaApiFields.BookingAllocInstructionID.value).get_parameters()
        alloc_id = actual_result[JavaApiFields.AllocationReportBlock.value][JavaApiFields.ClientAllocID.value]
        block_id = actual_result[JavaApiFields.AllocationReportBlock.value][JavaApiFields.AllocReportID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {JavaApiFields.PostTradeStatus.value:
                 self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).
                 get_parameters()[JavaApiFields.OrdUpdateBlock.value][JavaApiFields.PostTradeStatus.value]},
            'Comparing value after Allocation Instruction (step 2)')
        # endregion

        # region amend vat fees
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        print_message('Create Block', responses)
        new_misc_fee_rate = '3'
        fee_amount_new = str((float(fee_amount) / 2) * float(new_misc_fee_rate))
        root_misc_fees[JavaApiFields.RootMiscFeesBlock.value][0][JavaApiFields.RootMiscFeeAmt.value] = fee_amount_new
        root_misc_fees[JavaApiFields.RootMiscFeesBlock.value][0][
            JavaApiFields.RootMiscFeeRate.value] = new_misc_fee_rate
        self.allocation_instruction_message.update_fields_in_component("AllocationInstructionBlock",
                                                                       {
                                                                           'RootCommissionDataBlock': {
                                                                               'RootCommission': fee_amount_new,
                                                                               'RootCommType': 'A',
                                                                               'RootCommCurrency': misc_fee_curr
                                                                           },
                                                                           JavaApiFields.RootMiscFeesList.value: root_misc_fees,
                                                                           JavaApiFields.AllocInstructionID.value: block_id,
                                                                           JavaApiFields.AllocTransType.value: AllocTransTypes.AllocTransType_Replace.value,
                                                                           JavaApiFields.AllocType.value: AllocTypes.AllocType_P.value
                                                                       })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        print_message('Amend Block', responses)
        fee_amount_actually = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value). \
            get_parameters()[JavaApiFields.AllocationReportBlock.value][JavaApiFields.RootMiscFeesList.value][
            JavaApiFields.RootMiscFeesBlock.value][0][JavaApiFields.RootMiscFeeAmt.value]
        fee_amount_expected = {JavaApiFields.RootMiscFeeAmt.value: fee_amount_new}
        self.java_api_manager.compare_values(fee_amount_expected,
                                             {JavaApiFields.RootMiscFeeAmt.value: fee_amount_actually},
                                             'Comparing Fee amount after modify fee (step3)')
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
        actual_result = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]

        self.java_api_manager.compare_values(fee_amount_expected, {
            JavaApiFields.RootMiscFeeAmt.value: actual_result[JavaApiFields.MiscFeesList.value][
                JavaApiFields.MiscFeesBlock.value][0][JavaApiFields.MiscFeeAmt.value]},
                                             'Comparing Fee amount after allocate')
        print_message('Allocate block step 4', responses)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
