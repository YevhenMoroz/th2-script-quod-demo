import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3684(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.symbol = "test"
        self.lookup_symbol = "test"
        self.instr_symbol = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        page = ListingsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard = ListingsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_symbol(self.symbol)
        values_sub_wizard.set_lookup_symbol(self.lookup_symbol)
        values_sub_wizard.set_instr_symbol(self.instr_symbol)
        time.sleep(1)
        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_close()
        time.sleep(2)
        wizard.click_on_ok_button()
        time.sleep(2)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        values_sub_wizard = ListingsValuesSubWizard(self.web_driver_container)
        wizard = ListingsWizard(self.web_driver_container)
        self.verify("Is symbol field saved", self.symbol, values_sub_wizard.get_symbol())
        self.verify("Is lookup symbol field saved", self.lookup_symbol, values_sub_wizard.get_lookup_symbol())
        self.verify("Is instr_symbol field saved", self.instr_symbol, values_sub_wizard.get_instr_symbol())
        time.sleep(2)
        values_sub_wizard.set_symbol(" ")
        values_sub_wizard.set_lookup_symbol(" ")
        values_sub_wizard.set_instr_symbol(" ")
        time.sleep(2)
        wizard.click_on_close()
        time.sleep(2)
        wizard.click_on_ok_button()
