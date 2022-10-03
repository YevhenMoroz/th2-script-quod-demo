import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_T7283(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.recipient = Stubs.custom_config['qf_trading_fe_user']
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.order_type = OrderType.limit.value
        self.order_book_column = OrderBookColumns

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(self.order_book_column.order_id.value)

        # endregion

        # region accept order
        self.client_inbox.accept_order(self.lookup, self.qty, self.price)
        # endregion

        # region split CO order
        try:
            rule_manager = RuleManager(sim=Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                             self.data_set.
                                                                                             get_venue_client_names_by_name(
                                                                                                 'client_pt_1_venue_1'),
                                                                                             self.data_set.
                                                                                             get_mic_by_name(
                                                                                                 'mic_1'),
                                                                                             float(self.price))
            self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_1'), limit=self.price,
                                                qty=self.qty,
                                                order_type=self.order_type)
            self.order_ticket.split_limit_order()
        except Exception as E:
            logger.error(f'{E}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region set suspend option for CO order with cancelling of child order
        try:
            rule_manager = RuleManager(sim=Simulators.equity)
            cancel_trade_rule = rule_manager.add_OrderCancelRequest(bs_connectivity,
                                                                    self.data_set.get_venue_client_names_by_name(
                                                                        'client_pt_1_venue_1'),
                                                                    self.data_set.get_mic_by_name('mic_1'),
                                                                    True
                                                                    )
            self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_1'), limit=self.price,
                                                qty=self.qty,
                                                order_type=self.order_type)
            self.order_book.suspend_order(True, {self.order_book_column.order_id.value: order_id})
        except Exception as E:
            logger.error(f'{E}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(cancel_trade_rule)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region verify values after last action
        suspend_for_order = self.order_book.extract_field(self.order_book_column.suspend.value)
        self.order_book.compare_values({self.order_book_column.suspend.value: 'YES'},
                                       {self.order_book_column.suspend.value: suspend_for_order},
                                       'Comparing value at parent order')
        value_from_child = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                               [OrderBookColumns.sts.value], [1]
                                                               )

        self.order_book.compare_values({OrderBookColumns.sts.value: 'Cancelled'}, value_from_child[0],
                                       'Comparing of child order value')

        # endregion
