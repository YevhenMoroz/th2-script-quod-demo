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
    AllocationInstructionConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
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


class QAP_T7489(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '20000'
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
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        commission_profile = self.data_set.get_comm_profile_by_name('abs_amt')
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile,
                                                                         client=self.client)
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
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
            "ClOrdID": bca.client_orderid(9) + Path(__file__).name[:-3]
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region check statuses of order (precondition)
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
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
        exec_id = (actually_result[JavaApiFields.ExecID.value])
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                           JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}
        result = {JavaApiFields.TransExecStatus.value: actually_result[JavaApiFields.TransExecStatus.value],
                  JavaApiFields.PostTradeStatus.value: order_reply[JavaApiFields.PostTradeStatus.value]}
        self.java_api_manager.compare_values(expected_result, result, 'Check results from precondition')
        # endregion

        # region split book (step 1 step 2 and step 3)

        # send compute_request
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
        gross_trade_amt_common = str(int(self.qty) * float(new_avg_px))
        commission_rate = '1'
        fee_rate = '5'
        fee_amount = str(float(fee_rate) * float(gross_trade_amt_common) / 100)
        root_misc_fees = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.RootMiscFeesList.value]
        client_commission = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.ClientCommissionList.value]
        ### check fee and client commission
        client_commission_actual = client_commission[JavaApiFields.ClientCommissionBlock.value][0]
        root_misc_fees_actual = root_misc_fees[JavaApiFields.RootMiscFeesBlock.value][0]
        expected_client_commission = {
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value,
            JavaApiFields.CommissionAmount.value: str(float(commission_rate)),
            JavaApiFields.CommissionRate.value: str(float(commission_rate)),
            JavaApiFields.CommissionCurrency.value: self.currency_post_trade}
        expected_fees = {
            JavaApiFields.RootMiscFeeAmt.value: fee_amount,
            JavaApiFields.RootMiscFeeRate.value: str(float(fee_rate)),
            JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.RootMiscFeeType_EXC.value,
            JavaApiFields.RootMiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value
        }
        self.java_api_manager.compare_values(expected_client_commission, client_commission_actual,
                                             'Check client commission')
        self.java_api_manager.compare_values(expected_fees, root_misc_fees_actual, 'Check fee')
        ### end of checking
        # end of sending compute request

        # calculation and extracting needed values
        first_block_qty = int(self.qty) * 0.25
        seconds_block_qty = int(self.qty) * 0.75
        gross_trade_amt_split_first = float(float(gross_trade_amt_common) * 0.25)
        gross_trade_amt_split_second = float(float(gross_trade_amt_common) * 0.75)
        settl_curr_amt = float(gross_trade_amt_common) + float(commission_rate) + float(fee_amount)
        net_money_first = settl_curr_amt * 0.25
        net_money_second = settl_curr_amt * 0.75
        #  end of calculation
        dict_of_split_first = {"BookingQty": first_block_qty,
                               "NetGrossInd": "Gross",
                               "BookingType": "RegularBooking",
                               "SettlDate": datetime.utcnow().isoformat(),
                               "GrossTradeAmt": gross_trade_amt_split_first,
                               "NetMoney": str(net_money_first)}
        dict_of_split_second = {"BookingQty": seconds_block_qty,
                                "NetGrossInd": "Gross",
                                "BookingType": "RegularBooking",
                                "SettlDate": datetime.utcnow().isoformat(),
                                "GrossTradeAmt": gross_trade_amt_split_second,
                                "NetMoney": str(net_money_second)}
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock",
                                                               {'AvgPx': new_avg_px,
                                                                'Qty': self.qty,
                                                                "InstrID": instrument_id,
                                                                'Currency': self.currency_post_trade,
                                                                'GrossTradeAmt': gross_trade_amt_common,
                                                                'SettlCurrAmt': settl_curr_amt,
                                                                'RootCommissionDataBlock': {
                                                                    'RootCommission': fee_amount,
                                                                    'RootCommType': 'A',
                                                                    'RootCommCurrency': self.currency_post_trade
                                                                },
                                                                JavaApiFields.RootMiscFeesList.value: root_misc_fees,
                                                                JavaApiFields.ClientCommissionList.value: client_commission,
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': self.price}]},
                                                                'ComputeFeesCommissions':
                                                                    AllocationInstructionConst.ComputeFeesCommissions_N.value,
                                                                "AllocationInstructionQtyList":
                                                                    {"AllocationInstructionQtyBlock":
                                                                         [dict_of_split_first, dict_of_split_second]}
                                                                })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message('Split Booking order', responses)
        # endregion

        # region step 4 check fee and client commission in blocks
        list_of_qty = [str(first_block_qty), str(seconds_block_qty)]
        for qty in list_of_qty:
            if list_of_qty.index(qty) == 0:
                multiplier = 0.25
            else:
                multiplier = 0.75
            rate_and_amt = str(float(commission_rate)*multiplier)
            print(str(float(qty)))
            allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, f"'Qty': '{str(float(qty))}'").get_parameters()[JavaApiFields.AllocationReportBlock.value]
            client_commission_actual = allocation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
            fee_actual = allocation_report[JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value][0]
            expected_client_commission.update({JavaApiFields.CommissionRate.value: rate_and_amt,
                                               JavaApiFields.CommissionAmount.value: rate_and_amt})
            expected_fees.update({JavaApiFields.RootMiscFeeAmt.value: str(float(fee_amount) * multiplier)})
            self.java_api_manager.compare_values(expected_client_commission, client_commission_actual,
                                                 f'Check client commission for {list_of_qty.index(qty)+1} block (step5)')
            self.java_api_manager.compare_values(expected_fees, fee_actual,
                                                 f'Check fee for {list_of_qty.index(qty) + 1} block (step 5)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
