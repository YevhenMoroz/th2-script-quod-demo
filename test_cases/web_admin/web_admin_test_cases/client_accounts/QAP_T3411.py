import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard

from test_framework.web_admin_core.pages.client_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.client_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3411(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.desk = 'DESK A'
        self.assigned_user_to_desk = ''
        self.all_user_manager_entities = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_desks_page()
        desk_page = DesksPage(self.web_driver_container)
        desk_page.set_name_filter(self.desk)
        time.sleep(1)
        desk_page.click_on_more_actions()
        desk_page.click_on_edit()
        desk_assignments_tab = DesksAssignmentsSubWizard(self.web_driver_container)
        self.assigned_user_to_desk = desk_assignments_tab.get_all_assigned_users()

        side_menu.open_clients_page()

    def test_context(self):
        try:
            self.precondition()

            client_page = ClientsPage(self.web_driver_container)
            client_page.click_on_new()

            client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            self.all_user_manager_entities = client_assignments_tab.get_all_user_manager_from_drop_menu()

            self.verify("Users from other boards are displayed", True,
                        len(self.assigned_user_to_desk) != len(self.all_user_manager_entities))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
