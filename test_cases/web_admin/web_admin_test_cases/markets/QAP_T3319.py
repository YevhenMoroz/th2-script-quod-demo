import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_default_sub_wizard import VenuesDefaultSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3319(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = self.data_set.get_venue_type("venue_type_1")
        self.settlement_time = ['23:59:59', '20:50:58']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        side_menu.open_venues_page()
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_id(self.id)
        description_sub_wizard.set_client_venue_id(self.client_venue_id)
        description_sub_wizard.set_type(self.type)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            default_tab = VenuesDefaultSubWizard(self.web_driver_container)
            default_tab.set_settlement_time(self.settlement_time[1])

            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_revert_changes()
            time.sleep(0.5)
            self.verify("Settlement time has been revert", self.settlement_time[0], default_tab.get_settlement_time())
            wizard.click_on_save_changes()
            page.set_name_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            self.verify("Settlement time not changed", self.settlement_time[0], default_tab.get_settlement_time())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
