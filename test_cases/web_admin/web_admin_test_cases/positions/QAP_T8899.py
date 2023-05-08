import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_page import WashBookPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8899(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)
        cash_positions_page = MainPage(self.web_driver_container)
        wash_book_rules_page = WashBookRulesPage(self.web_driver_container)
        wash_book_page = WashBookPage(self.web_driver_container)

        try:
            self.precondition()

            position_tab_icon_attributes = side_menu.get_position_tab_icon_attributes()
            side_menu.open_cash_positions_page()
            time.sleep(1)
            self.verify("Cash Positions main page has the same icon as parent tab",
                        position_tab_icon_attributes, cash_positions_page.get_page_icon_attributes())
            side_menu.open_washbook_rules_page()
            time.sleep(1)
            self.verify("Wash Book Rules main page has the same icon as parent tab",
                        position_tab_icon_attributes, wash_book_rules_page.get_page_icon_attributes())
            side_menu.open_washbook_page()
            time.sleep(1)
            self.verify("Wash Book Rules main page has the same icon as parent tab",
                        position_tab_icon_attributes, wash_book_page.get_page_icon_attributes())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
