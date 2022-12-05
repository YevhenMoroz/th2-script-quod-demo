import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7141(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message_first = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_second = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.un_book_orders = BookingCancelRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA orders via FIX (part of precondition)
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            # first order
            self.fix_message_first.set_default_dma_limit()
            self.fix_message_first.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response_first = self.fix_manager.send_message_and_receive_response(self.fix_message_first)
            # get Client Order ID and Order ID
            order_id_first = response_first[0].get_parameters()['OrderID']

            # second order
            self.fix_message_second.set_default_dma_limit()
            self.fix_message_second.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response_second = self.fix_manager.send_message_and_receive_response(self.fix_message_second)
            # get Client Order ID and Order ID
            order_id_second = response_second[0].get_parameters()['OrderID']
        finally:
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region book DMA orders precondtidion and step 1
        list_of_alloc_instruction_ids = []
        list_of_order_ids = [order_id_first, order_id_second]
        gross_trade_amt = str(float(self.qty) * float(self.price))
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_2')
        for order_id in list_of_order_ids:
            self.allocation_instruction.set_default_book(order_id)
            self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
                "AvgPx": self.price,
                "AccountGroupID": self.client,
                "SettlCurrAmt": gross_trade_amt,
                'Side': 'Sell',
                'InstrID': instrument_id
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
            print_message(f'Book {order_id} order', responses)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            list_of_alloc_instruction_ids.append(allocation_report[JavaApiFields.ClBookingRefID.value])
            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            expected_result = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value}
            self.java_api_manager.compare_values(expected_result, order_update,
                                                 'Check expected and actually results from step 1',
                                                 VerificationMethod.CONTAINS)
        # endregion

        # region step 2 and step 3
        for alloc_id_instruction in list_of_alloc_instruction_ids:
            self.un_book_orders.set_default(alloc_id_instruction)
            responses = self.java_api_manager.send_message_and_receive_response(self.un_book_orders)
            print_message(
                f'Unbook {list_of_order_ids[list_of_alloc_instruction_ids.index(alloc_id_instruction)]} order',
                responses)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            expected_result = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}
            self.java_api_manager.compare_values(expected_result, order_update,
                                                 f'Check PostTradeStatus for '
                                                 f'{list_of_order_ids[list_of_alloc_instruction_ids.index(alloc_id_instruction)]} '
                                                 f'(part of step 3)',
                                                 VerificationMethod.CONTAINS)
            self.java_api_manager.compare_values(
                {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_CXL.value},
                allocation_report, 'Check AllocStatus (part of step 3)')
        # endregion
