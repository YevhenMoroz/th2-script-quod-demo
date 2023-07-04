import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3683(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = "test"
        self.id = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_id(self.id)
        time.sleep(1)
        wizard = VenuesWizard(self.web_driver_container)
        wizard.click_on_close()
        time.sleep(2)
        wizard.click_on_ok_button()
        time.sleep(2)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        self.verify("Is name field saved", self.name, description_sub_wizard.get_name())
        self.verify("Is id field saved", self.id, description_sub_wizard.get_id())
        time.sleep(2)
        description_sub_wizard.set_name(" ")
        description_sub_wizard.set_id(" ")
        time.sleep(2)
        wizard.click_on_close()
        time.sleep(2)
        wizard.click_on_ok_button()
