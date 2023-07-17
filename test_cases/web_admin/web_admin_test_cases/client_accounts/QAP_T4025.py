import time
import random
import string

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard import \
    ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4025(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T4025'
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.disclose_exec = 'Manual'
        self.desk = data_set.get_desk("desk_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        page = ClientsPage(self.web_driver_container)
        page.set_name(self.name)
        time.sleep(1)
        if not page.is_searched_client_found(self.name):
            page.click_on_new()
            values_tab = ClientsValuesSubWizard(self.web_driver_container)
            values_tab.set_id(self.id)
            values_tab.set_name(self.name)
            values_tab.set_ext_id_client(self.ext_id_client)
            values_tab.set_description(self.description)
            values_tab.set_disclose_exec(self.disclose_exec)
            assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
            assignments_tab.set_desk(self.desk)
            wizard = ClientsWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            page.set_name(self.name)
            time.sleep(1)

        page.click_on_more_actions()
        page.click_on_edit()

    def test_context(self):
        self.precondition()

        values_tab = ClientsValuesSubWizard(self.web_driver_container)
        values_tab.set_description(self.new_description)
        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()

        page = ClientsPage(self.web_driver_container)
        page.set_name(self.name)
        time.sleep(1)
        self.verify("Client has been changed", True, page.is_searched_client_found(self.name))
