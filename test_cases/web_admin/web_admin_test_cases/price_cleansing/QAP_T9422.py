import sys
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.main_page import MainPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.wizards import *
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T9422(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_rate_deviation_page()

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        self.precondition()

        main_page = MainPage(self.web_driver_container)
        main_page.click_on_more_actions()
        main_page.click_on_edit()
        values_tab = ValuesTab(self.web_driver_container)
        reference_venue = values_tab.get_reference_venues().split(",")[0]
        values_tab.click_at_reference_venue_by_name(reference_venue)
        time.sleep(1)
        venue_wizard = VenuesWizard(self.web_driver_container)
        venue_id = venue_wizard.get_venue_id()

        self.verify("Venue page open after click at Reference Venue", True, reference_venue == venue_id)
