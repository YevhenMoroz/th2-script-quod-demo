import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_description_sub_wizard import \
    VenuesDescriptionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4862(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
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
        description_sub_wizard = VenuesDescriptionSubWizard(self.web_driver_container)
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

        try:
            self.precondition()
            description_sub_wizard = VenuesDescriptionSubWizard(self.web_driver_container)
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

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
