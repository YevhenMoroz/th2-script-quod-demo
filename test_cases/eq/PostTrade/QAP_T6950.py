import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6950(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.error(f"{ex}", exc_info=True, stack_info=True)

        finally:
            time.sleep(3)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion

        # region verify value of fields after trade (precondition)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        value_done_for_day = self.order_book.extract_field(OrderBookColumns.done_for_day.value)
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: 'ReadyToBook', OrderBookColumns.done_for_day.value: 'Yes'},
            {OrderBookColumns.post_trade_status.value: post_trade_status,
             OrderBookColumns.done_for_day.value: value_done_for_day}, 'Comparing values after trade'
        )
        # endregion

        # region book order(precondition)
        self.middle_office.book_order()
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        # endregion

        # region approve and allocate block (step 1 and 2)
        self.middle_office.approve_block()
        values_of_middle_office = self.middle_office.extract_list_of_block_fields([
            MiddleOfficeColumns.sts.value,
            MiddleOfficeColumns.match_status.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched'}, values_of_middle_office,
                                          'Comparing values after approve for block of MiddleOffice')
        allocation_values = [{"Security Account": self.data_set.get_account_by_name('client_pt_1_acc_1'),
                              "Alloc Qty": qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_values)
        fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        fix_confirmation = FixMessageConfirmationReportOMS(self.data_set)
        fix_confirmation.set_default_confirmation_new(self.fix_message)
        self.middle_office.allocate_block()
        values_of_middle_office = self.middle_office.extract_list_of_block_fields([
            MiddleOfficeColumns.conf_service.value,
            MiddleOfficeColumns.sts.value,
            MiddleOfficeColumns.match_status.value,
            MiddleOfficeColumns.summary_status.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.summary_status.value: 'MatchedAgreed',
                                           MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched',
                                           MiddleOfficeColumns.conf_service.value: 'Manual'}, values_of_middle_office,
                                          'Comparing values after allocate for block of MiddleOffice')
        allocation_status = self.middle_office.extract_allocate_value(AllocationsColumns.sts.value)
        allocation_match_status = self.middle_office.extract_allocate_value(AllocationsColumns.match_status.value)
        self.middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'}, allocation_status,
                                          'Comparing allocation status')
        self.middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, allocation_match_status,
                                          'Comparing allocation match_status')
        fix_confirmation.add_tag({'Account': '*'})
        fix_confirmation.add_tag({'AllocInstructionMiscBlock2': '*'})
        fix_confirmation.add_tag({'tag5120': '*'})
        fix_verifier.check_fix_message_fix_standard(fix_confirmation)
        # endregion
