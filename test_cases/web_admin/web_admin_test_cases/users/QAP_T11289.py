import random
import string
import time
from datetime import datetime

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_venue_trader_sub_wizard import UsersVenueTraderSubWizard
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11289(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.db_manager = db_manager
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = '2@2'
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.venue_trade_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        venues_trade_tab = UsersVenueTraderSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_users_page()
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        if not users_page.is_searched_user_found(self.user_id):
            users_page.click_on_new_button()
            values_tab.set_user_id(self.user_id)
            values_tab.set_ext_id_client(self.ext_id_client)
            details_tab.set_mail(self.email)
            venues_trade_tab.click_on_plus_button()
            venues_trade_tab.set_venue(self.venue)
            venues_trade_tab.set_venue_trader_name(self.venue_trade_name)
            venues_trade_tab.set_expiry_date(datetime.today().strftime("%m/%d/%Y"))
            venues_trade_tab.click_on_checkmark_button()
            wizard.click_on_save_changes()
            time.sleep(1)
        else:
            self.db_manager.my_db.execute(
                f"UPDATE USERROLESVENUETRADER SET ALIVE = 'Y' WHERE USERID = '{self.user_id}'")
            time.sleep(1)

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        venues_trade_tab = UsersVenueTraderSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        try:
            self.precondition()

            users_page.set_user_id(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            time.sleep(2)
            self.verify("Venue Trade tab contains entries",
                        True, venues_trade_tab.is_venue_trader_tab_contains_entries())
            venues_trade_tab.click_on_delete_button()
            time.sleep(0.5)
            wizard.click_on_save_changes()
            time.sleep(1)
            users_page.set_user_id(self.user_id)
            time.sleep(1)
            users_page.click_on_more_actions()
            users_page.click_on_edit_at_more_actions()
            time.sleep(1)
            self.verify("Venue Trader entries has been deleted",
                        False, venues_trade_tab.is_venue_trader_tab_contains_entries())
        finally:
            self.db_manager.my_db.execute(
                f"UPDATE USERROLESVENUETRADER SET ALIVE = 'Y' WHERE USERID = '{self.user_id}'")


