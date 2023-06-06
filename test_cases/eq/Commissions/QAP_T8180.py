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
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
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


class QAP_T8180(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '300'
        self.price = '2'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.settl_currency = self.data_set.get_currency_by_name('currency_4')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_com_1_venue_1')
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
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        client_list = self.data_set.get_client_list('cl_list_comm_1')
        venue_list = self.data_set.get_venue_list('venue_list_1')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        commission = self.data_set.get_commission_by_name("commission1")
        self.rest_commission_sender.clear_commissions()
        params = {
            'clCommissionID': commission.value,
            'clCommissionName': commission.name,
            'commissionAmountType': "BRK",
            'commissionProfileID': commission_profile,
            'recomputeInConfirmation': 'false',
            'clientListID': client_list,
            'venueListID': venue_list,
            'settlCurrency': self.settl_currency
        }
        self.rest_commission_sender.set_modify_client_commission_message(params)
        self.rest_commission_sender.send_post_request()

        # endregion

        # region create DMA  orders (step 1)
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
            "ClOrdID": bca.client_orderid(9) + Path(__file__).name[:-3],
            'SettlCurrFxRate': '0',
            'SettlCurrency': self.settl_currency

        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region trade DMA order (step 2)
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
        rate = float(5)
        commission_amount = rate * float(self.qty) * float(self.price) / 10000
        expected_commission = {
            JavaApiFields.CommissionAmount.value: str(commission_amount),
            JavaApiFields.CommissionCurrency.value: self.currency_post_trade,
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionRate.value: str(rate),
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_PCT.value
        }
        client_commission = \
            actually_result[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(expected_commission, client_commission, 'check results of step 2')
        # endregion

        # region step 3
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
        client_commission = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.ClientCommissionList.value]
        self.java_api_manager.compare_values(expected_commission,
                                             client_commission[JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check results of step 3')
        # endregion

        # region step 4
        self.allocation_instruction_message.set_default_book(order_id)
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        self.allocation_instruction_message.update_fields_in_component('AllocationInstructionBlock',
                                                                       {
                                                                           'GrossTradeAmt': gross_currency_amt,
                                                                           'AvgPx': new_avg_px,
                                                                           'Qty': self.qty,
                                                                           'AccountGroupID': self.client,
                                                                           'Currency': self.currency_post_trade,
                                                                           "InstrID": instrument_id,
                                                                           JavaApiFields.ClientCommissionList.value: client_commission,
                                                                           'ExecAllocList': {
                                                                               'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                                   'ExecID': exec_id,
                                                                                                   'ExecPrice': self.price}]},

                                                                       })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
        print_message('Create Block', responses)
        # endregion
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(expected_commission,
                                             allocation_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check results of step 4')

        # region approve and allocate block
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
        print_message('Allocate Block ', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(expected_commission,
                                             confirmation_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'check expected result from step 5')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
