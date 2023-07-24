import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_page import AutoHedgerPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3524(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_auto_hedger_page()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        main_page = AutoHedgerPage(self.web_driver_container)
        try:
            main_page.click_on_disabled()
            self.verify("Is auto hedger disabled", True, True)
        except Exception as e:
            self.verify("Auto hedger is not disabled", True, e.__class__.__name__)
        time.sleep(2)
        try:
            main_page.click_on_enable()
            self.verify("Is auto hedger enabled", True, True)
        except Exception as e:
            self.verify("Auto hedger is not enabled", True, e.__class__.__name__)

