import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_page import WashBookPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3352(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.firm_account = 'ACABankFirm'
        self.institution_account = 'ACABankInst'
        self.wash_book_account = 'ACAWashbook'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_washbook_page()

    def test_context(self):
        try:
            self.precondition()

            wash_book_page = WashBookPage(self.web_driver_container)
            wash_book_page.set_id_filter(self.firm_account)
            time.sleep(1)
            self.verify(f"Firm Account {self.firm_account} not displayed", False,
                        wash_book_page.is_searched_entity_found(self.firm_account))
            wash_book_page.set_id_filter(self.institution_account)
            time.sleep(1)
            self.verify(f"Institution Account {self.institution_account} not displayed", False,
                        wash_book_page.is_searched_entity_found(self.institution_account))
            wash_book_page.set_id_filter(self.wash_book_account)
            time.sleep(1)
            self.verify(f"WashBook Account {self.wash_book_account} displayed", True,
                        wash_book_page.is_searched_entity_found(self.wash_book_account))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
