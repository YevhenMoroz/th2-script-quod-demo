import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_page import \
    QuotingSessionsPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_values_sub_wizard import \
    QuotingSessionsValuesSubWizard
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_wizard import \
    QuotingSessionsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_1758(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = str
        self.published_quote_id_format = "#20d"
        self.quote_update_format = "FullRefresh"


def precondition(self):
    login_page = LoginPage(self.web_driver_container)
    login_page.login_to_web_admin(self.login, self.password)
    side_menu = SideMenu(self.web_driver_container)
    time.sleep(2)
    side_menu.open_quoting_sessions_page()
    page = QuotingSessionsPage(self.web_driver_container)
    time.sleep(1)
    page.click_on_more_actions()
    time.sleep(2)
    page.click_on_edit()
    time.sleep(2)
    values_sub_wizard = QuotingSessionsValuesSubWizard(self.web_driver_container)
    self.name = values_sub_wizard.get_name()
    wizard = QuotingSessionsWizard(self.web_driver_container)
    wizard.click_on_save_changes()
    time.sleep(2)
    page.set_name_filter(self.name)
    time.sleep(2)
    page.click_on_more_actions()
    time.sleep(2)


def test_context(self):
    try:
        self.precondition()
        page = QuotingSessionsPage(self.web_driver_container)
        try:
            page.click_on_delete(True)
            time.sleep(15)
            # region relogin web admin
            common_page = CommonPage(self.web_driver_container)
            common_page.click_on_user_icon()
            time.sleep(2)
            common_page.click_on_logout()
            time.sleep(2)
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.login, self.password)
            side_menu = SideMenu(self.web_driver_container)
            time.sleep(2)
            side_menu.open_quoting_sessions_page()
            # endregion
            page.set_name_filter(self.name)
            time.sleep(2)
            page.click_on_edit()
            self.verify("Entity not deleted !! ERROR", True, False)
        except Exception:
            self.verify("Entity deleted ", True, True)


    except Exception:
        basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                          status='FAILED')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
        print(" Search in ->  " + self.__class__.__name__)
