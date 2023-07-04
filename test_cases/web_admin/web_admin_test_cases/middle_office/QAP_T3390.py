import random
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_dimensions_sub_wizard import FeesDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3390(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(1)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()
        time.sleep(1)
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()

    def test_context(self):

        self.precondition()
        time.sleep(2)
        fees_dimension_tab = FeesDimensionsSubWizard(self.web_driver_container)
        fees_dimension_tab.set_venue(random.choice(fees_dimension_tab.get_all_venue_from_drop_menu()))
        time.sleep(1)
        self.verify("Venue List field become disable", False, fees_dimension_tab.is_venue_list_field_enable())
        time.sleep(1)
        fees_dimension_tab.set_venue("Not found")
        time.sleep(1)
        fees_dimension_tab.set_venue_list(random.choice(fees_dimension_tab.get_all_venue_list_from_drop_menu()))
        time.sleep(1)
        self.verify("Venue field become disable", False, fees_dimension_tab.is_venue_field_enable())
