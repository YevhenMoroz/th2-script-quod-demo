import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.reference_data.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from test_framework.web_admin_core.pages.reference_data.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.reference_data.subvenues.subvenues_wizard import SubVenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_760(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = "AMEX"
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_venue = "ASE"

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
        wizard = SubVenuesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        description_sub_wizard.set_name(self.new_name)
        time.sleep(1)
        description_sub_wizard.set_venue(self.new_venue)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name_filter(self.new_name)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = SubVenuesPage(self.web_driver_container)
            actual_values_from_main_page = [page.get_name(), page.get_venue()]
            except_values_from_main_page = [self.new_name,
                                            self.new_venue]
            self.verify("Is entity edited correctly", except_values_from_main_page, actual_values_from_main_page)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
