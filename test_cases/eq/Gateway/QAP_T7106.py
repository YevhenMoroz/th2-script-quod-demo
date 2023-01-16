import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7106(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        class_name = QAP_T7106
        qty = '6154'
        price = '6154'
        alloc_acount = self.data_set.get_account_by_name('client_pt_1_acc_1')
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_tag_5120'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        fix_varifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        trade_rule = None
        new_order_single_rule = order_id = None
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.test_id, status='FAIL')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region book order and verify values after it at order book (step 1)
        list_of_ignored_fields = ['Account', 'SettlCurrency', 'OrderAvgPx']
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_2")
        settl_currency_amt = str(int(qty) * int(price))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': settl_currency_amt,
                                                                   'AvgPx': price,
                                                                   'Qty': qty,
                                                                   "InstrID": instrument_id
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        class_name.print_message('BOOK', responses)
        fix_allocation_instruction = FixMessageAllocationInstructionReportOMS()
        fix_allocation_instruction.set_default_ready_to_book(self.fix_message)
        fix_allocation_instruction.add_tag({'tag5120': 'test123'})
        fix_allocation_instruction.add_tag({'RootSettlCurrAmt': '*'})
        fix_varifier.check_fix_message_fix_standard(fix_allocation_instruction, ignored_fields=list_of_ignored_fields)
        actually_post_trade_status = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameter('OrdUpdateBlock')[
                'PostTradeStatus']
        alloc_id = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            'AllocationReportBlock')['ClientAllocID']
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {OrderBookColumns.post_trade_status.value: actually_post_trade_status},
            'Comparing actual and expected result from step 4, 5')
        # endregion

        # region approve block and verifying values after that (step 2)
        self.approve_message.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        class_name.print_message('APPROVE', responses)
        # endregion

        # region allocate order and verifying it via FIX
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": alloc_acount,
            'AllocQty': qty,
            'AvgPx': price,
            "InstrID": instrument_id,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        class_name.print_message('ALLOCATE BLOCK', responses)
        fix_allocation_instruction.set_default_preliminary(self.fix_message)
        fix_allocation_instruction.change_parameter('NoAllocs', '*')
        fix_varifier.check_fix_message_fix_standard(fix_allocation_instruction, ignored_fields=list_of_ignored_fields)
        fix_confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        fix_confirmation_message.set_default_confirmation_new(self.fix_message)
        fix_confirmation_message.add_tag({'Account': '*'})
        fix_confirmation_message.add_tag({'tag5120': 'test123'})
        fix_varifier.check_fix_message_fix_standard(fix_confirmation_message, ignored_fields=list_of_ignored_fields)
        # endregion

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
