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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
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


class QAP_2973(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        no_allocs: dict = {'NoAllocs': [
            {
                'AllocAccount': self.data_set.get_account_by_name('client_pt_1_acc_1'),
                'AllocQty': qty
            }]}
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        list_of_extraction_value = [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
                                    MiddleOfficeColumns.settl_currency.value, MiddleOfficeColumns.exchange_rate.value,
                                    MiddleOfficeColumns.settl_curr_fx_rate_calc.value]
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create and execute order (precondition)
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region book order (step 1, step 2)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.middle_office.set_modify_ticket_details(settl_currency='UAH', exchange_rate='2',
                                                     exchange_rate_calc='Multiply', toggle_recompute=True)
        self.middle_office.book_order()
        values_of_block = self.middle_office.extract_list_of_block_fields(list_of_extraction_value,
                                                                           row_number=1,
                                                                           filter_list=[OrderBookColumns.order_id.value,
                                                                                        order_id])
        self.middle_office.compare_values({list_of_extraction_value[0]: 'ApprovalPending',
                                           list_of_extraction_value[1]: 'Unmatched',
                                           list_of_extraction_value[2]: 'UAH',
                                           list_of_extraction_value[3]: '2',
                                           list_of_extraction_value[4]: 'M'
                                           }, values_of_block, 'Comparing value after book order')
        # endregion

        # region (step 3, step 4)
        self.middle_office.approve_block()
        self.middle_office.ex
        # endregion
