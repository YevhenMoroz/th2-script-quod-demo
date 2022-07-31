import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, \
    SecondLevelTabs, ChildOrderBookColumns, MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7082(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client('client_pt_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.lookup = self.data_set.get_lookup_by_name('lookup_2')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1 , 2)
        qty = '1000'
        price = '10'
        new_order_rule = trade_rule = None
        alt_accounts = {'test1': '50', 'test2': '50'}
        venue = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        try:
            new_order_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, client, venue, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client, venue, float(price),
                                                                                            int(qty), delay=0
                                                                                            )
            self.order_ticket.set_order_details(client=self.client, qty=qty, limit=price,
                                                alloc_details=alt_accounts, set_alt_account=True)
            self.order_ticket.create_order(self.lookup)
        except Exception as e:
            logger.error(f"{e}", exc_info=True, stack_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check expected result of step 1
        expected_result = [{'Id': 'test2'}, {'Id': 'test1'}]
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        value = self.order_book.extract_fields_list({OrderBookColumns.order_id.value: OrderBookColumns.order_id.value,
                                                     OrderBookColumns.sts.value: OrderBookColumns.sts.value})
        order_id = value.pop(OrderBookColumns.order_id.value)
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.terminated.value}, value,
                                       'Comparing value of order from step 1 and step 2')

        values = self.order_book.extract_2lvl_fields(SecondLevelTabs.pre_trade_alloc_tab.value,
                                                     [ChildOrderBookColumns.id_allocation.value], [1, 2], filter_dict)
        for index in range(len(values)):
            if expected_result.__contains__(values[index]):
                self.order_book.compare_values({'2': '2'}, {'2': '2'},
                                               'Comparing  PreAllocationTab from  step 1')
        # endregion

        # region step 3 and 4
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.middle_office.book_order(filter_list)
        # endregion

        # region step 5
        filter_dict_of_block = {MiddleOfficeColumns.order_id.value: order_id}
        filter_list_of_block = [MiddleOfficeColumns.order_id.value, order_id]
        self.middle_office.approve_block()
        self.middle_office.allocate_block(filter_list_of_block)
        # endregion
        for alt_account in alt_accounts.keys():
            values = self.middle_office.extract_list_of_allocate_fields(
                [AllocationsColumns.alt_account.value, AllocationsColumns.alloc_qty.value],
                {AllocationsColumns.alt_account.value: alt_account}, filter_dict_block=filter_dict_of_block,
                clear_filter_from_block=True, clear_filter_from_allocation=True)
            expected_result = {AllocationsColumns.alt_account.value: alt_account,
                               AllocationsColumns.alloc_qty.value: str(int(int(qty) / 2))}
            self.middle_office.compare_values(expected_result, values, 'Comparing values from step 5')
        # endregion
