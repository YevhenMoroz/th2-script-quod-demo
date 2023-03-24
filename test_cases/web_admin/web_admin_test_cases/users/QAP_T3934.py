import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_venue_trader_sub_wizard import UsersVenueTraderSubWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3934(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.user_id = self.data_set.get_user("user_6")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_trader_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.set_user_id(self.user_id)
        time.sleep(2)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)
        venue_trader_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
        venue_trader_wizard.click_on_plus_button()
        venue_trader_wizard.set_venue(self.venue)
        venue_trader_wizard.set_venue_trader_name(self.venue_trader_name)
        venue_trader_wizard.click_on_checkmark_button()
        time.sleep(2)

    def post_conditions(self):
        venue_trader_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
        venue_trader_wizard.click_on_delete_button()
        users_wizard = UsersWizard(self.web_driver_container)
        users_wizard.click_on_save_changes()

    def test_context(self):
        users_wizard = UsersWizard(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        venue_trader_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
        try:
            self.precondition()
            expected_pdf_content = [self.venue, self.venue_trader_name]
            try:
                self.verify(f"Is PDF contains {expected_pdf_content}", True,
                            users_wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
            except Exception as e:
                self.verify(f"PDF is not contains {expected_pdf_content}", True, e.__class__.__name__)

            users_wizard.click_on_save_changes()

            users_page.set_user_id(self.user_id)
            time.sleep(2)
            users_page.click_on_more_actions()
            time.sleep(2)
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            actual_result = [venue_trader_wizard.get_venue(), venue_trader_wizard.get_venue_trader_name()]

            try:
                self.verify("Venue is saved correctly", [self.venue, self.venue_trader_name], actual_result)
            except Exception as e:
                self.verify("Venue saved incorrectly", True, e.__class__.__name__)
            time.sleep(2)
            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
