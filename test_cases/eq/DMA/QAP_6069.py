import datetime
import logging
import os
import random
import string
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import BaseWindow, decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
"""
IgnoreTradeDate=false at ex.xml
"""


class QAP6069(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_6069(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_message = FixMessageNewOrderSingleOMS()
        fix_message.set_default_dma_limit()
        client = fix_message.get_parameter('Account')
        price = fix_message.get_parameter('Price')
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        trade_date = str(datetime.date.today() + datetime.timedelta(days=3)).replace('-', '')
        default_trade_date = str(datetime.date.today()).replace('-', '')
        # endregion

        # region Open FE
        base_window.open_fe(self.report_id, work_dir, username, password)
        # endregion

        # region create DMA order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             'XPAR_' + client,
                                                                                             'XPAR', float(price))
            trade_with_trade_date = \
                rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQtyWithTradeDate_FIXStandard(
                    self.bs_connectivity,
                    'XPAR_' + client, 'XPAR', float(price), int(qty), trade_date, delay=0)
            fix_manager.send_message_fix_standard(fix_message)
            order_id_first = order_book.extract_field('Order ID')
        # endregion
        finally:
            time.sleep(1)
            rule_manager.remove_rule(trade_with_trade_date)
            rule_manager.remove_rule(nos_rule)

        # region extract executions from orders
        extracted_values_first_order = order_book.extract_2lvl_fields('Executions', ['Qty', 'TradeDate'], [1],
                                                                      {'Order ID': order_id_first})

        # endregion
        extracted_values_first_order[0]['TradeDate'] = \
            str(extracted_values_first_order[0]['TradeDate']).replace('/', '')
        expected_result_first = {'Qty': '100', 'TradeDate': default_trade_date}
        base_window.compare_values(expected_result_first,
                                   extracted_values_first_order[0], 'Check values of First Order')

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_6069()
