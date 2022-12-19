import random
import string
import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venue_lists.main_page import VenueListsPage
from test_framework.web_admin_core.pages.markets.venue_lists.wizard import VenuesListsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7932(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_list = ["BATS", "BINANCE"]
        self.basic_fields = ["Name", 'Description']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venue_list_page()

    def test_context(self):
        main_page = VenueListsPage(self.web_driver_container)
        wizard = VenuesListsWizard(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new()

            self.verify("The PDF file contains all fields name with/without data", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.basic_fields))

            wizard.set_name(self.name)
            wizard.set_description(self.description)
            wizard.set_venue_list(self.venue_list)

            self.verify("The PDF file contains all fields name with/without data", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.venue_list + self.basic_fields))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
