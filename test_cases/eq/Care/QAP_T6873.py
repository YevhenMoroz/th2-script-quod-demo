import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageCancelRejectReportOMS import FixMessageOrderCancelRejectReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6873(TestCase):
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
        self.bag_order_book = OMSBagOrderBook(self.case_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_modify_message = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.fix_cancel_reject = FixMessageOrderCancelRejectReportOMS()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '100'
        second_qty = '400'
        error_qty = '900'
        price = '10'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        venue_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        cl_ord_id = self.fix_message.get_parameter("ClOrdID")
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_modify_message.set_default(self.fix_message)
        self.fix_modify_message.change_parameter('OrderQtyData', {'OrderQty': second_qty})
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        self.fix_cancel_reject.set_default(self.fix_message)
        filter_dict = {'ClOrdID': cl_ord_id}
        filter_dict_inbox = {'ClOrdId': cl_ord_id}
        filter_list = []
        for obj, values in filter_dict.items():
            filter_list.append(obj)
            filter_list.append(values)
        nos_rule = modification_rule = None
        # endregion

        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        self.client_inbox.accept_order(lookup, qty, price,
                                       filter=filter_dict_inbox)
        # endregion

        # region split CO order and verify values
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  venue_account,
                                                                                                  exec_destination,
                                                                                                  float(price))
            self.order_ticket.split_order(filter_list=filter_list)
            self.__extract_field_and_comparing_from_child_and_parent(OrderBookColumns.unmatched_qty.value,
                                                                     filter_list=filter_list, expected_parent_field='0')
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region send modify and accept it
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequestWithDelayFixStandard(
                self.fix_env.buy_side,
                venue_account,
                exec_destination,
                True, delay=10000)
            self.fix_manager.send_message_fix_standard(fix_message=self.fix_modify_message)
            self.client_inbox.accept_modify_plus_child()
            self.fix_modify_message.change_parameter('OrderQtyData', {'OrderQty': error_qty})
            self.fix_manager.send_message_fix_standard(fix_message=self.fix_modify_message)
            self.fix_verifier.check_fix_message_fix_standard(self.fix_cancel_reject)
            self.__extract_field_and_comparing_from_child_and_parent(OrderBookColumns.unmatched_qty.value,
                                                                     filter_dict=filter_dict,
                                                                     filter_list=filter_list,
                                                                     expected_field_child=second_qty,
                                                                     field_child=OrderBookColumns.qty.value,
                                                                     expected_parent_field='0')
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(80)
            self.rule_manager.remove_rule(modification_rule)
        # endregion

    def __extract_field_and_comparing_from_child_and_parent(self, field_parent: str, filter_dict=None, filter_list=None,
                                                            expected_field_child: str = None, field_child: str = None,
                                                            expected_parent_field=None):
        self.order_book.set_filter(filter_list=filter_list)
        value = self.order_book.extract_field(field_parent)
        if field_child and filter_dict and expected_field_child:
            value_child = \
                self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value, [field_child], [1],
                                                    filter_dict=filter_dict)[
                    0][
                    field_child]
            self.order_book.compare_values({field_parent: expected_field_child},
                                           {field_parent: value_child},
                                           f'Comparing {field_child} Child order')
        self.order_book.compare_values({field_parent: expected_parent_field},
                                       {field_parent: value},
                                       f'Comparing {field_parent} of Parent order')
