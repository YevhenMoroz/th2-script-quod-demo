import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard import \
    ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3307(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = self.data_set.get_disclose_exec("disclose_exec_1")
        self.desks = 'Quod Desk'
        self.assigned_user_to_desk = []
        self.user_manager = str

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_desks_page()
        desk_page = DesksPage(self.web_driver_container)
        desk_page.set_name_filter(self.desks)
        time.sleep(1)
        desk_page.click_on_more_actions()
        desk_page.click_on_edit()
        assignments_tab = DesksAssignmentsSubWizard(self.web_driver_container)
        self.assigned_user_to_desk = assignments_tab.get_all_assigned_users()
        side_menu.open_clients_page()

    def test_context(self):
        self.precondition()

        page = ClientsPage(self.web_driver_container)
        page.click_on_new()
        wizard_values = ClientsValuesSubWizard(self.web_driver_container)
        wizard_values.set_id(self.id)
        wizard_values.set_name(self.name)
        wizard_values.set_disclose_exec(self.disclose_exec)
        wizard_values.set_ext_id_client(self.ext_id_client)

        wizard_assignments = ClientsAssignmentsSubWizard(self.web_driver_container)
        wizard_assignments.set_desk(self.desks)
        user_manager = wizard_assignments.get_all_user_manager_from_drop_menu()
        self.user_manager = random.choice(user_manager)
        while True:
            if self.user_manager in self.assigned_user_to_desk:
                self.user_manager = random.choice(user_manager)
            else: break

        wizard_assignments.set_user_manager(self.user_manager)
        wizard_page = ClientsWizard(self.web_driver_container)
        wizard_page.click_on_save_changes()

        common_act = CommonPage(self.web_driver_container)

        time.sleep(1)
        self.verify("User is not save, error appears", True, common_act.is_error_message_displayed())
