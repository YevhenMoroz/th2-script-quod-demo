import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import BaseWindow, decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_6110(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_6110(self):
        # region Declaration
        base_window = BaseMainWindow(self.case_id, self.session_id)
        oms_order_book = OMSOrderBook(self.case_id, self.session_id)
        oms_middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        price = '1000'
        client = 'MOClient'
        fix_message = FixMessageNewOrderSingleOMS()
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_message.set_default_dma_limit()
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        fix_message.change_parameter('Price', price)
        fix_message.change_parameter('Account', client)
        fix_message.change_parameter("Instrument", Instrument.ISI3.value)
        fix_message.change_parameter("ExDestination", Instrument.ISI3.value.get('SecurityExchange'))
        fix_message.change_parameter('Currency', 'GBp')
        # endregion
        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion

        # region create 2  DMA order and execute them
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_EUREX",
                                                                                             'XEUR', float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + '_EUREX', 'XEUR',
                                                                                       float(price), int(qty), 0)
            fix_manager.send_message_fix_standard(fix_message)
            order_id_first = oms_order_book.extract_field('Order ID')
            oms_order_book.scroll_order_book(1)
        except Exception:
            logger.info('Oh shit, I am sorry')

        finally:
            time.sleep(3)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion

        # region mass book orders
        oms_middle_office.book_order()
        # endregion

        # region verify value
        extracting_price_first_order = oms_middle_office.extract_block_field('Net Price', ['Order ID', order_id_first])
        extracting_qty_first_order = oms_middle_office.extract_block_field('Qty')
        oms_middle_office.compare_values({'Net Price': '10'}, extracting_price_first_order,
                                         'Check first block Net Price')
        oms_middle_office.compare_values({'Qty': qty}, extracting_qty_first_order, 'Check first block qty')

        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_6110()
