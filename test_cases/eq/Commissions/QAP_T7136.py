import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, PositionValidities, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7136(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_com_1')
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.mic = self.data_set.get_mic_by_name('mic_2')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_modification = OrderModificationRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set up needed fees and backend configuration
        # part 1: set needed fees
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_by_name("venue_2")
        fee_type_agent = self.data_set.get_misc_fee_type_by_name('agent')
        perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.rest_commission_sender.set_modify_fees_message(comm_profile=perc_amt, fee_type=fee_type_agent)
        self.rest_commission_sender.change_message_params({'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        fee_3 = self.data_set.get_fee_by_name('fee3')
        fee_type_exch_fees = self.data_set.get_misc_fee_type_by_name('exch_fees')
        bas_amt = self.data_set.get_comm_profile_by_name('bas_amt')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=bas_amt, fee_type=fee_type_exch_fees,
                                                            fee=fee_3)
        self.rest_commission_sender.change_message_params({'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # end_of_part

        # part 2: Set configuration for Agent fees
        self.ssh_client.send_command("/home/quod317/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(80)
        # end_of_part
        # endregion

        # region step 1: Split CO order
        # part 1: Create CO order
        currency = self.data_set.get_currency_by_name('currency_3')
        qty = '10000'
        price = '10'
        self.fix_message.set_default_care_limit(instr='instrument_3', account='client_com_1')
        self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': qty},
                                            'Price': price,
                                            'Currency': currency})
        responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = responses[0].get_parameter("OrderID")
        cl_ord_id = responses[0].get_parameter("ClOrdID")
        # end_of_part

        # part 2: Split CO order and trade child DMA order
        self.order_submit.set_default_child_dma(order_id)
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        listing_id = self.data_set.get_listing_id_by_name('listing_2')
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]},
            JavaApiFields.InstrID.value: instrument_id,
            JavaApiFields.Currency.value: currency,
            JavaApiFields.OrdQty.value: qty,
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.Price.value: price
        })
        self._split_co_order(qty, price, order_id)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_first = execution_report[JavaApiFields.ExecID.value]
        fee_agent_rate = '5.0'
        agent_fees_amount = str(float(qty) * float(price) * float(fee_agent_rate) / 10000)
        exch_fees_amount = str(float(qty) * float(price) / 1000000)
        currency_GBP = self.data_set.get_currency_by_name('currency_2')
        fees_list = execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value]
        self._sort_fee_list(fees_list, JavaApiFields.MiscFeeAmt.value)
        exch_fees_dict = {JavaApiFields.MiscFeeAmt.value: exch_fees_amount,
                          JavaApiFields.MiscFeeBasis.value: ExecutionReportConst.MiscFeeBasis_B.value,
                          JavaApiFields.MiscFeeCurr.value: currency_GBP, JavaApiFields.MiscFeeRate.value: '1.0',
                          JavaApiFields.MiscFeeType.value: ExecutionReportConst.MiscFeeType_EXC.value}
        agent_fees_dict = {JavaApiFields.MiscFeeAmt.value: agent_fees_amount,
                           JavaApiFields.MiscFeeBasis.value: ExecutionReportConst.MiscFeeBasis_P.value,
                           JavaApiFields.MiscFeeCurr.value: currency_GBP,
                           JavaApiFields.MiscFeeRate.value: fee_agent_rate,
                           JavaApiFields.MiscFeeType.value: ExecutionReportConst.MiscFeeType_AGE.value}
        self.java_api_manager.compare_values(exch_fees_dict, fees_list[0],
                                             'Verify that ExchFees properly calculated (step 1)')
        self.java_api_manager.compare_values(agent_fees_dict, fees_list[1],
                                             'Verify that AgentFees properly calculated (step 1)')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verify that order is filled (step 1)')
        # end_of_part
        # endregion

        # region step 2: Amend CO order
        self.order_modification.set_default(self.data_set, order_id)
        doubled_qty = str(float(qty) * 2)
        self.order_modification.update_fields_in_component(JavaApiFields.OrderModificationRequestBlock.value,
                                                           {JavaApiFields.AccountGroupID.value: self.client,
                                                            JavaApiFields.OrdQty.value: doubled_qty,
                                                            JavaApiFields.PosValidity.value: PositionValidities.PosValidity_DEL.value,
                                                            JavaApiFields.WashBookAccountID.value: self.data_set.get_washbook_account_by_name(
                                                                'washbook_account_3'),
                                                            JavaApiFields.Price.value: price})
        self.java_api_manager.send_message_and_receive_response(self.order_modification, response_time=20000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: str(float(qty))},
                                             order_reply,
                                             f'Verify that order has {JavaApiFields.UnmatchedQty.value} that equals {qty} (step 3)')
        # endregion

        # region step 3: Split CO order again
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.ClOrdID.value: bca.client_orderid(9)})
        self._split_co_order(qty, price, order_id)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_second = execution_report[JavaApiFields.ExecID.value]
        fees_list = execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value]
        self._sort_fee_list(fees_list, JavaApiFields.MiscFeeAmt.value)
        self.java_api_manager.compare_values(exch_fees_dict, fees_list[0],
                                             'Verify that ExchFees properly calculated (step 3)')
        self.java_api_manager.compare_values(agent_fees_dict, fees_list[1],
                                             'Verify that AgentFees properly calculated (step 3)')
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report, 'Verify that order is filled (step 3)')
        # endregion

        # region step 4: Book CO order
        # part 1: Complete CO order
        self.complete_message.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_message)
        # end_of_part

        # part 2: Send ComputeBookingFeesCommissionsRequest
        new_avg_px = float(price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_ord_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(qty, exec_id_first, price, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(qty, exec_id_second, price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(doubled_qty, new_avg_px, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        exch_fees_dict = {JavaApiFields.RootMiscFeeAmt.value: str(float(exch_fees_amount) * 2),
                          JavaApiFields.RootMiscFeeBasis.value: ExecutionReportConst.MiscFeeBasis_B.value,
                          JavaApiFields.RootMiscFeeCurr.value: currency_GBP,
                          JavaApiFields.RootMiscFeeRate.value: '1.0',
                          JavaApiFields.RootMiscFeeType.value: ExecutionReportConst.MiscFeeType_EXC.value}
        agent_fees_dict = {JavaApiFields.RootMiscFeeAmt.value: str(float(agent_fees_amount) * 2),
                           JavaApiFields.RootMiscFeeBasis.value: ExecutionReportConst.MiscFeeBasis_P.value,
                           JavaApiFields.RootMiscFeeCurr.value: currency_GBP,
                           JavaApiFields.RootMiscFeeRate.value: fee_agent_rate,
                           JavaApiFields.RootMiscFeeType.value: ExecutionReportConst.MiscFeeType_AGE.value}
        fees_list = compute_reply[JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value]
        print(fees_list)
        self._sort_fee_list(fees_list, JavaApiFields.RootMiscFeeAmt.value)
        print(fees_list)
        self.java_api_manager.compare_values(exch_fees_dict, fees_list[0],
                                             'Verify that ExchFees properly calculated (step 4) ComputeBookingFeesCommissionsRequest')
        self.java_api_manager.compare_values(agent_fees_dict, fees_list[1],
                                             'Verify that AgentFees properly calculated (step 4) ComputeBookingFeesCommissionsRequest')
        # end_of_part

        # part 3: Send AllocationReport
        self.allocation_instruction_message.set_default_book(order_id)
        self.allocation_instruction_message.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                                       {
                                                                           JavaApiFields.AvgPx.value: new_avg_px,
                                                                           JavaApiFields.Qty.value: doubled_qty,
                                                                           JavaApiFields.AccountGroupID.value: self.client,
                                                                           JavaApiFields.Currency.value: currency_GBP,
                                                                           JavaApiFields.InstrID.value: instrument_id,
                                                                           JavaApiFields.RootMiscFeesList.value: {
                                                                               JavaApiFields.RootMiscFeesBlock.value: [
                                                                                   agent_fees_dict, exch_fees_dict]},
                                                                           JavaApiFields.ExecAllocList.value: {
                                                                               JavaApiFields.ExecAllocBlock.value: [
                                                                                   {JavaApiFields.ExecQty.value: qty,
                                                                                    JavaApiFields.ExecID.value: exec_id_first,
                                                                                    JavaApiFields.ExecPrice.value: price},
                                                                                   {JavaApiFields.ExecQty.value: qty,
                                                                                    JavaApiFields.ExecID.value: exec_id_second,
                                                                                    JavaApiFields.ExecPrice.value: price}
                                                                               ]},
                                                                       })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, f'Verify that order has {JavaApiFields.PostTradeStatus.value} = {OrderReplyConst.PostTradeStatus_BKD.value} (step 4)')
        fees_list = allocation_report[JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value]
        self._sort_fee_list(fees_list, JavaApiFields.RootMiscFeeAmt.value)

        self.java_api_manager.compare_values(exch_fees_dict, fees_list[0],
                                             'Verify that ExchFees properly calculated (step 4) for Block')
        self.java_api_manager.compare_values(agent_fees_dict, fees_list[1],
                                             'Verify that AgentFees properly calculated (step 4) for Block')
        # end_of_part
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.send_command("/home/quod317/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(90)

    def _split_co_order(self, qty, price, order_id):
        new_order_single = trade_rule = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client, self.mic, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client, self.mic,
                                                                                            float(price), int(qty), 0)
            self.java_api_manager.send_message_and_receive_response(self.order_submit, filter_dict={order_id: order_id},
                                                                    response_time=20000)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            if new_order_single is not None and trade_rule is not None:
                self.rule_manager.remove_rule(new_order_single)
                self.rule_manager.remove_rule(trade_rule)

    def _sort_fee_list(self, fee_list, field):
        for counter in range(len(fee_list)):
            minimum = counter
            for counter_2 in range(counter + 1, len(fee_list)):
                if fee_list[counter_2][field] < fee_list[counter][
                    field]:
                    minimum = counter_2
            fee_list[minimum], fee_list[counter] = fee_list[counter], fee_list[minimum]
