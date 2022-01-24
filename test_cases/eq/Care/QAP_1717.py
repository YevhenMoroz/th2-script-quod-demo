import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_1717(TestCase):
    def __init__(self, report_id, session_id, dataset):
        super().__init__(report_id, session_id, dataset)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        client = self.data_set.get_client_by_name('client_pt_1')
        price = '100'
        qty = '50'
        qty_percent = '100'
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        user = Stubs.custom_config['qf_trading_fe_user']
        # endregion

        # region create CO order
        order_ticket.set_order_details(client=client, limit=price, qty=qty, tif='Day', recipient=user,
                                       partial_desk=True)
        order_ticket.create_order(self.data_set.get_lookup_by_name('lookup_1'))
        order_id_first = order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion

        # region accept CO order
        client_inbox.accept_order(lookup, qty, price)
        # endregion

        # region Direct CO order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
                                                                                             self.data_set.get_venue_client_names_by_name(
                                                                                                 'client_pt_1_venue_1'),
                                                                                             self.data_set.get_mic_by_name(
                                                                                                 'mic_1'), float(price)
                                                                                             )
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(bs_connectivity,
                                                                           self.data_set.get_venue_client_names_by_name(
                                                                               'client_pt_1_venue_1'),
                                                                           self.data_set.get_mic_by_name(
                                                                               'mic_1'), float(price), int(qty), delay=0
                                                                           )
            order_book.direct_order_correct(lookup, qty, price, qty_percent)
        except Exception as e:
            logger.error(f'{e} your exception')
        finally:
            time.sleep(3)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)

        # endregion

        # region extract values from second level tab
        # region extraction_value
        order_book.set_filter([OrderBookColumns.order_id.value, order_id_first])
        result = order_book.extract_2lvl_fields('Child Orders',
                                                [OrderBookColumns.sts.value, OrderBookColumns.qty.value], rows=[1])
        order_book.compare_values({OrderBookColumns.sts.value: 'Open', OrderBookColumns.qty.value: qty}, result[0],
                                  'Equals values')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
