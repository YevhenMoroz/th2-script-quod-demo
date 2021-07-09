import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_venue_trader_sub_wizard import UsersVenueTraderSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2256(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.user_id = "adm01"
        self.venue = "JSE"
        self.venue_trader_name = "AW9RSTOWN03_03426"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm02")
        login_page.set_password("adm02")
        login_page.click_login_button()
        login_page.check_is_login_successful()
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
        venue_trader_wizard = UsersVenueTraderSubWizard(self.web_driver_container)
        venue_trader_wizard.click_on_plus_button()
        venue_trader_wizard.set_venue(self.venue)
        venue_trader_wizard.set_venue_trader_name(self.venue_trader_name)
        venue_trader_wizard.click_on_checkmark_button()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        users_wizard = UsersWizard(self.web_driver_container)
        expected_pdf_content = [self.venue, self.venue_trader_name]

        self.verify(f"Is PDF contains {expected_pdf_content}", True,
                    users_wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
