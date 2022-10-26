import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_features_sub_wizard import \
    VenuesFeaturesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3115(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = "QAP_T3115"
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = "DarkPool"
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.open_time = ['00:00:00', '01:01:01']
        self.close_time = ['23:59:59', '02:02:02']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        page = VenuesPage(self.web_driver_container)
        page.set_name_filter(self.name)
        time.sleep(1)
        if not page.is_searched_venue_found(self.name):
            page.click_on_new()
            values_tab = VenuesValuesSubWizard(self.web_driver_container)
            values_tab.set_name(self.name)
            values_tab.set_id(self.id)
            values_tab.set_type(self.type)
            values_tab.set_client_venue_id(self.client_venue_id)
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            page.set_name_filter(self.name)
            time.sleep(1)

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.click_on_more_actions()
            time.sleep(1)
            page.click_on_edit()
            features_tab = VenuesFeaturesSubWizard(self.web_driver_container)
            features_tab.set_open_time(self.open_time[0])
            features_tab.set_close_time(self.close_time[0])
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            self.verify("Open and Close time has been save", [self.open_time[0], self.close_time[0]],
                        [features_tab.get_open_time(), features_tab.get_close_time()])

            features_tab.set_open_time(self.open_time[1])
            features_tab.set_close_time(self.close_time[1])
            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
