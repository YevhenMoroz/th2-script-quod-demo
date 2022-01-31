import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, SecondLevelTabs, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_6181(TestCase):
    def __init__(self, report_id, session_id, date_set):
        super().__init__(report_id, session_id, date_set)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        fix_manager = FixManager(ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = fix_message.get_parameter('Price')
        order_type = OrderType.limit.value
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        # endregion

        # # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        # endregion

        # region accept CO orders
        client_inbox.accept_order(lookup, qty, price)
        # endregion

        # region split order
        try:
            rule_manager = RuleManager(sim=Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                                 self.data_set.get_venue_client_names_by_name('client_1_venue_1'),
                                                                                                 self.data_set.get_mic_by_name('mic_1'), float(price))

            order_ticket.set_order_details(self.data_set.get_client_by_name('client_1'), limit=price, qty=qty,
                                           order_type=order_type)
            order_ticket.split_limit_order()
        except Exception as E:
                logger.error(f'{E}')
        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region send modify request
        try:
            rule_manager.add_OrderCancelReplaceRequest_FIXStandard(bs_connectivity,
                                                        self.data_set.get_venue_client_names_by_name('client_1_venue_1'),
                                                        self.data_set.get_mic_by_name('mic_1'), True)
            fix_message_cancer_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set, fix_message.get_parameters())
            fix_message_cancer_replace.change_parameter('OrderQtyData', {'OrderQty': '50'})
            fix_message_cancer_replace.add_tag({'OrigClOrdID': fix_message.get_parameter("ClOrdID")})
            fix_manager.send_message_fix_standard(fix_message_cancer_replace)
                # region accept modify
            client_inbox.accept_modify_plus_child(lookup, qty, price)
            # endregion
        except Exception as E:
            logger.debug('Error Message' + {E})
        finally:
            time.sleep(3)

        # endregion

        # region verify order
        result_from_parent = order_book.extract_field(OrderBookColumns.qty.value)
        order_book.compare_values({OrderBookColumns.qty.value: '50'}, {OrderBookColumns.qty.value: result_from_parent},
                                  'Comparing Values Parent')
        result = order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value, [OrderBookColumns.qty.value,
                                                                                  OrderBookColumns.sts.value], [1])
        order_book.compare_values({OrderBookColumns.qty.value: '50',  OrderBookColumns.sts.value: 'Open'}, result[0],
                                  'Comparing Values Child')
        # endregion
