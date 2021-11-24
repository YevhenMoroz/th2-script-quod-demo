import logging
import os
import random
import string

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP4466(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_4466(self):
        # region Declaration
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        base_window = BaseWindow(self.case_id, self.session_id)
        basket_book = OMSBasketOrderBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        path_xlsx = "C:\\Users\\" + 'vskulinec' + '\\PycharmProjects\\th2-script-quod-demo(QUOD)\\quod_qa\\eq\\Basket' \
                                                  '\\Basket_import_files\\testDummyValues2.xlsx'
        # endregion

        # region Open FE
        cl_inbox.open_fe(self.report_id, work_dir, username, password)
        # endregion

        # region create basket with remove first order
        result_expected = basket_book.basket_row_details(row_filter='100', remove_row=True)
        basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        basket_book.create_basket_via_import(basket_name, basket_template_name='Test Template', path=path_xlsx,
                                             client='MOClient', amend_rows_details=[result_expected])
        # endregion

        # region extract value from basket order
        result = basket_book.get_basket_orders_values(2, 'Qty')
        expected = {'1': '200', '2': '300'}
        base_window.compare_values(expected, result, 'Check Qty')
        # endregion

    # @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4466()
