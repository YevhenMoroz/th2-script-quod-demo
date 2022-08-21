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
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, SecondLevelTabs, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7099(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_manager = FixManager(environment.get_list_fix_environment()[0].sell_side)
        self.bs_connectivity = environment.get_list_fix_environment()[0].buy_side
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.order_type = OrderType.limit.value
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        # endregion
        self.client_inbox.accept_order(filter_dict)
        # region split order
        try:
            rule_manager = RuleManager(sim=Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             self.data_set.get_venue_client_names_by_name(
                                                                                                 'client_1_venue_1'),
                                                                                             self.data_set.get_mic_by_name(
                                                                                                 'mic_1'),
                                                                                             float(self.price))

            self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_1'), limit=self.price,
                                                qty=self.qty,
                                                order_type=self.order_type)
            self.order_ticket.split_limit_order()
        except Exception as E:
            logger.error(f'{E}')
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region send modify request
        try:
            rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                   self.data_set.get_venue_client_names_by_name(
                                                                       'client_1_venue_1'),
                                                                   self.data_set.get_mic_by_name('mic_1'), True)
            fix_message_cancer_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set,
                                                                                self.fix_message.get_parameters())
            fix_message_cancer_replace.change_parameter('OrderQtyData', {'OrderQty': '50'})
            fix_message_cancer_replace.add_tag({'OrigClOrdID': self.fix_message.get_parameter("ClOrdID")})
            self.fix_manager.send_message_fix_standard(fix_message_cancer_replace)
            # region accept modify
            self.client_inbox.accept_modify_plus_child(filter_dict)
            # endregion
        except Exception as E:
            logger.debug('Error Message' + {E})
        finally:
            time.sleep(1)

        # endregion

        # region verify order
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list({OrderBookColumns.qty.value: '50'})
        result = self.order_book.extract_sub_lvl_fields([OrderBookColumns.qty.value, OrderBookColumns.sts.value],
                                                        [SecondLevelTabs.child_tab.value], filter_dict)
        self.order_book.compare_values({OrderBookColumns.qty.value: '50', OrderBookColumns.sts.value: ExecSts.open.value},
                                       result, 'Comparing Values Child')
        # endregion
