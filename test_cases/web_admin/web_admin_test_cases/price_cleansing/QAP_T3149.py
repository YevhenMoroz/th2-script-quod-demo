import sys
import time
import traceback
import random
import string
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.main_page import MainPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.wizards import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3149(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.price_deviation = random.randint(1, 100)

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_rate_deviation_page()
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = ValuesTab(self.web_driver_container)
        values_tab.set_name(self.name)
        values_tab.set_reference_venues(random.choice(values_tab.get_all_reference_venues_from_drop_menu()))
        values_tab.set_price_deviation(self.price_deviation)
        wizard = MainWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):

        self.precondition()

        main_page = MainPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)
        time.sleep(1)
        self.verify("Entity has been delete", False, main_page.is_searched_entity_found_by_name(self.name))

