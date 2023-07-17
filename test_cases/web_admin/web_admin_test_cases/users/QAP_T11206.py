import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import \
    UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_routes_sub_wizard import \
    UsersRoutesSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11206(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.db_manager = db_manager

        self.email = '2@2'
        self.user_id = self.__class__.__name__
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = [self.data_set.get_route("route_1"), self.data_set.get_route("route_2")]
        self.rote_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.first_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_venue = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        route_tab = UsersRoutesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
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
            route_tab.click_on_plus_button()
            route_tab.set_route(self.route[0])
            route_tab.set_route_user_name(self.rote_name)
            route_tab.click_on_checkmark_button()
            time.sleep(0.5)
            route_tab.click_on_plus_button()
            route_tab.set_route(self.route[1])
            route_tab.set_route_user_name(self.rote_name)
            route_tab.click_on_checkmark_button()
            time.sleep(0.5)
            wizard.click_on_save_changes()

        self.db_manager.my_db.execute(f"UPDATE ROUTEUSERROLES SET ALIVE = 'Y' WHERE USERID = '{self.user_id}'")

    def test_context(self):
        users_page = UsersPage(self.web_driver_container)
        values_tab = UsersValuesSubWizard(self.web_driver_container)
        details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
        route_tab = UsersRoutesSubWizard(self.web_driver_container)
        wizard = UsersWizard(self.web_driver_container)

        self.precondition()

        users_page.set_user_id(self.user_id)
        time.sleep(1)
        users_page.click_on_more_actions()
        users_page.click_on_edit_at_more_actions()
        values_tab.set_ext_id_venue(self.ext_id_venue)
        details_tab.set_first_name(self.first_name)
        routes_in_table = route_tab.get_all_route_in_table()
        route_tab.click_on_delete_button_for_last_entry_in_table()
        wizard.click_on_save_changes()
        users_page.set_user_id(self.user_id)
        time.sleep(1)
        users_page.click_on_more_actions()
        users_page.click_on_edit_at_more_actions()
        time.sleep(1)
        self.verify("User Ext Id Venue is changed", self.ext_id_venue, values_tab.get_ext_id_venue())
        self.verify("Firs Name is changed", self.first_name, details_tab.get_first_name())
        self.verify("Deleted Route is not displayed",
                    False, routes_in_table[-1] in route_tab.get_all_route_in_table())
