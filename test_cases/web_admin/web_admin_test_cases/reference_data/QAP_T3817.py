import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3817(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_venue_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.type = self.data_set.get_venue_type("venue_type_1")
        self.country = self.data_set.get_country("country_1")
        self.new_country = self.data_set.get_country("country_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = VenuesWizard(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        time.sleep(1)
        description_sub_wizard.set_id(self.id)
        description_sub_wizard.set_client_venue_id(self.client_venue_id)
        time.sleep(1)
        description_sub_wizard.set_type(self.type)
        time.sleep(1)
        description_sub_wizard.set_country(self.country)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        description_sub_wizard.set_country(self.new_country)
        time.sleep(1)

    def test_context(self):
        try:
            self.precondition()
            page = VenuesPage(self.web_driver_container)
            wizard = VenuesWizard(self.web_driver_container)
            expected_pdf_content = [self.name,
                                    self.id,
                                    self.type,
                                    self.new_country,
                                    ]
            self.verify("Is pdf contains correctly values before saving", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name_filter(self.name)
            time.sleep(2)
            expected_values_from_main_page = [self.name,
                                              self.id,
                                              self.new_country,
                                              ]
            actual_values_from_main_page = [page.get_name(), page.get_id(), page.get_country()]

            self.verify("Is main page contains correctly values",
                        expected_values_from_main_page,
                        actual_values_from_main_page)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
