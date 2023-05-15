import logging
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    JavaApiFields, ExecutionReportConst, AllocationInstructionConst, OrderReplyConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9336(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.bas_amt = self.data_set.get_comm_profile_by_name("bas_amt")
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        instr_type = self.data_set.get_instr_type('mutual_fund')
        fee_type = self.data_set.get_misc_fee_type_by_name('regulatory')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.perc_amt, fee_type=fee_type)
        self.rest_commission_sender.change_message_params({'instrType': instr_type, "venueID": self.data_set.get_venue_by_name("venue_1")})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client, comm_profile=self.bas_amt)
        self.rest_commission_sender.send_post_request()
        # endregion

        # region step 1-2: Create DMA order
        new_order_single = trade_rule = None
        self.submit_request.set_default_dma_limit()
        listing_id = self.data_set.get_listing_id_by_name('listing_9')
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_8')
        self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ListingList.value: {JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]},
            JavaApiFields.InstrID.value: instrument_id,
            JavaApiFields.AccountGroupID.value: self.client
        })
        qty = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        price = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        fee_rate = '5.0'
        fee_amount = str(float(qty) * float(price)/100 * float(fee_rate))
        commission_rate = '1.0'
        commission_amount = str(float(qty) * float(price)/10000)
        expected_result_client_commission = {JavaApiFields.CommissionAmount.value: commission_amount,
                                             JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
                                             JavaApiFields.CommissionBasis.value:AllocationInstructionConst.COMM_AND_FEE_BASIS_BPS.value,
                                             JavaApiFields.CommissionRate.value: commission_rate}
        expected_result_fees = {JavaApiFields.MiscFeeAmt.value: fee_amount,
                                JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
                                JavaApiFields.MiscFeeRate.value: fee_rate}
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity, self.venue_client, self.mic, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity, self.venue_client, self.mic, float(price), int(qty), 0)
            self.java_api_manager.send_message_and_receive_response(self.submit_request, response_time=15_000)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, OrderReplyConst.TransStatus_OPN.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                                 order_reply, 'Verify that order created (step 1)')
            execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(expected_result_client_commission, execution_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0],
                                                 'Verify that Client commission was calculated (step 2)')
            self.java_api_manager.compare_values(expected_result_fees,
                                                 execution_report[JavaApiFields.MiscFeesList.value][
                                                     JavaApiFields.MiscFeesBlock.value][0],
                                                 'Verify that Fees was calculated (step 2)')

        except Exception as e:
            logger.error(f'Something go wrong {e}')
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # enderegion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
