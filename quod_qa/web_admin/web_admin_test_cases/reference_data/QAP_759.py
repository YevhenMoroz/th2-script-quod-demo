import random
import string
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_page import SubVenuesPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_wizard import SubVenuesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_759(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMEX"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_subvenues_page()
        time.sleep(2)
        page = SubVenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        time.sleep(2)
        description_sub_wizard.set_venue(self.venue)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = SubVenuesPage(self.web_driver_container)
            wizard = SubVenuesWizard(self.web_driver_container)
            excepted_pdf_values = [self.name,
                                   "AMERICAN STOCK EXCHANGE"]
            self.verify("Is pdf correctly", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(excepted_pdf_values))
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name_filter(self.name)
            time.sleep(2)
            actual_values_from_main_page = [page.get_name(), page.get_venue()]
            excepted_values = [self.name,
                               self.venue]
            self.verify("Is entity edited correctly", excepted_values, actual_values_from_main_page)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
