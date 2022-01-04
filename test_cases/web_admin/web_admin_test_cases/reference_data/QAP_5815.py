import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.nested_wizards.venues_exchange_codes_sub_wizard import \
    VenuesExchangeCodesSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_description_sub_wizard import \
    VenuesDescriptionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5815(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.venue = "ASE"
        self.exchange_code_mic = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

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
        description_sub_wizard.click_on_mic_manage_button()
        exchange_codes_sub_wizard = VenuesExchangeCodesSubWizard(self.web_driver_container)
        exchange_codes_sub_wizard.click_on_plus_button()
        exchange_codes_sub_wizard.set_venue(self.venue)
        exchange_codes_sub_wizard.set_exchange_code_mic(self.exchange_code_mic)
        time.sleep(1)
        exchange_codes_sub_wizard.click_on_checkmark()
        time.sleep(2)
        wizard = VenuesWizard(self.web_driver_container)
        wizard.click_on_go_back_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            description_sub_wizard = VenuesDescriptionSubWizard(self.web_driver_container)
            description_sub_wizard.set_mic(self.exchange_code_mic)
            time.sleep(1)
            self.verify("Is MIC created correctly ", self.exchange_code_mic, description_sub_wizard.get_mic())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
