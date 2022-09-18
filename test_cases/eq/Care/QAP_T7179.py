import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, SecondLevelTabs, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7179(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.child_order_book = OMSChildOrderBook(self.test_id, self.session_id)
        self.fix_env = environment.get_list_fix_environment()[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        fix_manager = FixManager(self.fix_env.sell_side)
        fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = fix_message.get_parameter('Price')
        order_type = OrderType.limit.value
        cl_ord_id = fix_message.get_parameter('ClOrdID')
        filter_dict_for_order_and_client_blotter = {OrderBookColumns.cl_ord_id.value: cl_ord_id}
        # endregion

        # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        # endregion

        # region accept CO orders
        self.client_inbox.accept_order(filter_dict_for_order_and_client_blotter)
        # endregion
        #
        # region split order
        nos_rule = None
        rule_manager = RuleManager(sim=Simulators.equity)
        try:
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.data_set.get_venue_client_names_by_name(
                                                                                                 'client_1_venue_1'),
                                                                                             self.data_set.get_mic_by_name(
                                                                                                 'mic_1'), float(price))

            self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_1'), limit=price, qty=qty,
                                                order_type=order_type)
            self.order_ticket.split_limit_order()
        except Exception as E:
            logger.error(f'{E}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region extract order ID
        result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value, [OrderBookColumns.order_id.value],
                                                     [1],
                                                     filter_dict_for_order_and_client_blotter)
        # endregion

        # region verify, that child order is  appeared in child order book
        expected_result = {'Verify Result': 'Grid has orders!'}
        child_order_filter = {OrderBookColumns.order_id.value: result[0]['ID']}
        actually_result = self.child_order_book.checking_presence_of_order(child_order_filter)
        self.child_order_book.compare_values(expected_result, actually_result, 'Verifying values')
        # endregion

        # region verify, that child order is  appeared in child order book
        expected_result = {'Verify Result': 'Grid is empty!'}
        child_order_filter_list = [OrderBookColumns.order_id.value, result[0]['ID']]
        self.order_book.set_filter(child_order_filter_list)
        actually_result = self.order_book.extract_field(OrderBookColumns.sts.value, expected_empty_rows=True)
        self.child_order_book.compare_values(expected_result, actually_result, 'Verifying values')
        # endregion
