import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_venue_trader_sub_wizard import UsersVenueTraderSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2257(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.venue = "AMEX"
        self.new_venue_trader_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        time.sleep(2)
        users_page.click_on_more_actions()
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)
        venue_trader_sub_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
        venue_trader_sub_wizard.click_on_plus_button()
        time.sleep(2)
        venue_trader_sub_wizard.set_venue(self.venue)
        venue_trader_sub_wizard.set_venue_trader_name(self.new_venue_trader_name)
        venue_trader_sub_wizard.click_on_checkmark_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            users_wizard = UsersWizard(self.web_driver_container)
            venue_trader_sub_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
            users_page = UsersPage(self.web_driver_container)
            expected_pdf_content = [self.venue, self.new_venue_trader_name]

            self.verify(f"Is PDF contains {expected_pdf_content}", True,
                        users_wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            users_wizard.click_on_save_changes()
            time.sleep(2)
            users_page.click_on_more_actions()
            time.sleep(2)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            venue_trader_sub_wizard.click_on_delete_button()
            time.sleep(2)
            users_wizard.click_on_save_changes()
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
