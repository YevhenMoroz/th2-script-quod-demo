import sys
import time
import random
import string
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_routes_sub_wizard import UsersRoutesSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3292(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.user_id = "QAP_T3292"
        self.user_ext_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.email = 'a@a'
        self.desks = self.data_set.get_desk("desk_1")
        self.new_user_ext_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.routes = ''
        self.rote_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        main_page = UsersPage(self.web_driver_container)
        main_page.set_user_id(self.user_id)
        time.sleep(1)
        if not main_page.is_searched_user_found(self.user_id):
            main_page.click_on_new_button()
            value_tab = UsersValuesSubWizard(self.web_driver_container)
            value_tab.set_user_id(self.user_id)
            value_tab.set_ext_id_client(self.user_ext_id)
            user_details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
            user_details_tab.set_mail(self.email)
            assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.click_on_desks()
            assignments_tab.set_desks(self.desks)
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            main_page.set_user_id(self.user_id)
            time.sleep(1)

        main_page.click_on_more_actions()
        main_page.click_on_edit_at_more_actions()

    def test_context(self):

        try:
            self.precondition()

            routes_tab = UsersRoutesSubWizard(self.web_driver_container)
            routes_tab.click_on_plus_button()
            self.routes = random.choice(routes_tab.get_all_routes_from_drop_menu())
            routes_tab.set_route(self.routes)
            routes_tab.set_route_user_name(self.rote_name)
            routes_tab.click_on_checkmark_button()
            wizard = UsersWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page = UsersPage(self.web_driver_container)
            main_page.set_user_id(self.user_id)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit_at_more_actions()

            routes_tab.set_route_filter(self.routes)
            time.sleep(1)
            routes_tab.click_on_edit_button()

            self.verify("Rotes has been save", self.routes, routes_tab.get_route())

            routes_tab.click_on_cancel_button()
            routes_tab.click_on_delete_button()

            wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
