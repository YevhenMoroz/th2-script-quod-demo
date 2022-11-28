import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from datetime import datetime
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7132(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        commission_profile = self.data_set.get_comm_profile_by_name('per_u_qty')
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile,
                                                                         account=self.alloc_account)
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.clear_fees()
        fee = self.data_set.get_fee_by_name('fee3')
        commission_profile_fee = self.data_set.get_comm_profile_by_name('perc_amt')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile_fee, fee=fee)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
        })
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA  orders (precondition)
        list_of_client_order_ids = []
        side = 'Buy'
        list_of_order_ids = []
        for i in range(2):
            self.order_submit.set_default_dma_limit()
            if i > 0:
                side = "Sell"
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
                'InstrID': instrument_id,
                'AccountGroupID': self.client,
                'OrdQty': self.qty,
                'Side': side,
                'Price': self.price,
                "ClOrdID": bca.client_orderid(9) + Path(__file__).name[:-3],
                "PreTradeAllocationBlock": {
                    "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [{'AllocAccountID': self.alloc_account,
                                                                              'AllocQty': self.qty}]}}
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message('Create DMA  order', responses)
            list_of_order_ids.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
            list_of_client_order_ids.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value])
            # endregion

        # region check fee and client commissions of DMA orders (step 1)
        list_of_exec_ids = []
        fee_rate = '5.0'
        commission_rate = str(float(0.5))
        commission_amount = str(float(commission_rate) * float(self.qty) / 100)
        expected_client_commission = {
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_UNI.value,
            JavaApiFields.CommissionAmount.value: commission_amount,
            JavaApiFields.CommissionRate.value: commission_rate,
            JavaApiFields.CommissionCurrency.value: self.currency_post_trade}
        expected_fee = {
            JavaApiFields.MiscFeeAmt.value: commission_amount,
            JavaApiFields.MiscFeeRate.value: fee_rate,
            JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.MiscFeeType.value: AllocationInstructionConst.RootMiscFeeType_EXC.value,
            JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value
        }
        for order_id in list_of_order_ids:
            self.execution_report.set_default_trade(order_id)
            if list_of_order_ids.index(order_id) == 0:
                side = "Buy"
            else:
                side = 'Sell'
            self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                             {
                                                                 "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                     "instrument_2"),
                                                                 "Side": side,
                                                                 "LastTradedQty": self.qty,
                                                                 "VenueExecID": bca.client_orderid(9),
                                                                 "LastVenueOrdID": (
                                                                         tm(datetime.utcnow().isoformat()) + bd(
                                                                     n=2)).date().strftime(
                                                                     '%Y-%m-%dT%H:%M:%S'),
                                                                 "LastPx": self.price,
                                                                 "OrdType": "Limit",
                                                                 "Price": self.price,
                                                                 "Currency": self.currency,
                                                                 "ExecType": "Trade",
                                                                 "TimeInForce": "Day",
                                                                 "LeavesQty": self.qty,
                                                                 "CumQty": self.qty,
                                                                 "AvgPrice": self.price,
                                                                 "LastMkt": self.venue_mic,
                                                                 "OrdQty": self.qty
                                                             })
            responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
            print_message(f'Trade DMA  order {order_id}', responses)
            actually_result = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                       ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            list_of_exec_ids.append(actually_result[JavaApiFields.ExecID.value])
            commission_actually: dict = \
                actually_result[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
            fee_actually = actually_result[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0]
            self.java_api_manager.compare_values(expected_client_commission, commission_actually,
                                                 'Check that client commission correctly calculated (step 1)')
            self.java_api_manager.compare_values(expected_fee, fee_actually, 'Check fee from step 1')
            side = 'Buy'

        # endregion

        # region step 2
        expected_client_commission.pop(JavaApiFields.CommissionRate.value)
        expected_client_commission.update(
            {JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value})
        expected_fee.clear()
        expected_fee = {
            JavaApiFields.RootMiscFeeAmt.value: commission_amount,
            JavaApiFields.RootMiscFeeRate.value: commission_rate,
            JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.RootMiscFeeType_EXC.value,
            JavaApiFields.RootMiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value
        }
        new_avg_px = str(float(self.price) / 100)
        for order_id in list_of_order_ids:
            if list_of_order_ids.index(order_id) > 0:
                side = "Sell"
            else:
                side = "Buy"
            self.allocation_instruction.set_default_book(order_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                                   {
                                                                       'AvgPx': new_avg_px,
                                                                       'Qty': self.qty,
                                                                       'Side': side,
                                                                       "InstrID": instrument_id,
                                                                       'Currency': self.currency_post_trade,
                                                                       'ExecAllocList': {
                                                                           'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                               'ExecID':
                                                                                                   list_of_exec_ids[
                                                                                                       list_of_order_ids.index(
                                                                                                           order_id)],
                                                                                               'ExecPrice': self.price}]},
                                                                       'ComputeFeesCommissions':
                                                                           AllocationInstructionConst.ComputeFeesCommissions_Y.value,

                                                                   })
            responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
            print_message(f'Booking order {order_id}', responses)

            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            commission_actually = \
                allocation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
            self.java_api_manager.compare_values(expected_client_commission, commission_actually,
                                                 'Check that client commission didn`t change after book(step 2)')
            fee_actually = \
                allocation_report[JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value][0]
            self.java_api_manager.compare_values(expected_fee, fee_actually,
                                                 'Check that fee didn`t change after book(step 2)')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
