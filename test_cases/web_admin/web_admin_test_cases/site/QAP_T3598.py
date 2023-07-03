import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3598(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = self.data_set.get_location("location_3")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_locations_page()
        time.sleep(2)
        location_page = LocationsPage(self.web_driver_container)
        location_page.set_name(self.name)
        time.sleep(2)
        location_page.click_on_enable_disable_button()
        time.sleep(1)

    def test_context(self):
        self.precondition()
        location_page = LocationsPage(self.web_driver_container)
        try:
            location_page.click_on_enable_disable_button()
            self.verify("Location enabled", True, True)

        except Exception as e:
            self.verify("Location not enabled", True, e.__class__.__name__)
