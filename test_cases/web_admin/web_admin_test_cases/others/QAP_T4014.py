import random
import string
import sys
import time
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4014(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        time.sleep(2)
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.click_on_new()
        time.sleep(2)
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)
        counterparts_wizard.set_name_value_at_values_tab(self.name)
        time.sleep(1)
        counterparts_wizard.click_on_save_changes()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()
        time.sleep(2)
        counterparts_main_menu = CounterpartsPage(self.web_driver_container)
        counterparts_main_menu.set_name_filter_value(self.name)
        time.sleep(1)
        self.verify("Counterpart entity is present", "True",
                    counterparts_main_menu.is_counterpart_present_by_name(self.name))
        counterparts_main_menu.click_on_more_actions()
        time.sleep(1)
        counterparts_main_menu.click_on_delete_and_confirmation(True)
        time.sleep(2)
        self.verify("Counterparts deleted", "False",
                    counterparts_main_menu.is_counterpart_present_by_name(self.name))