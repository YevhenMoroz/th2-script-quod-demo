import logging
import os
import random
import string

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP6114(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_6114(self):
        # region Declaration
        bas_book = OMSBasketOrderBook(self.case_id, self.session_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        basket_template_name = "Test Template"
        client = "CLIENT_FIX_CARE"
        path_xlsx = "C:\\Users\\" + username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                               '\\Basket_import_files\\BasketTemplate_withHeader_expending_values.xlsx'
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Create basket
        bas_book.create_basket_via_import(basket_name, basket_template_name, path_xlsx, client)
        # endregion
        # region Check Basket book
        ord_types = bas_book.get_basket_orders_value(2, "OrdType", {"Basket Name": basket_name})
        bas_book.compare_values({'1': 'Limit', '2': 'Limit'}, ord_types, "Compare ord types")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_6114()
