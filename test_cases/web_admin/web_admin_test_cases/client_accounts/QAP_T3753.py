import time
import random
import string

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_wizard import ClientsWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_values_sub_wizard \
    import ClientsValuesSubWizard
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3753(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"

        self.disclose_exec = "Manual"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk = data_set.get_desk("desk_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()

    def test_context(self):
        self.precondition()

        main_page = ClientsPage(self.web_driver_container)
        main_page.click_on_new()
        values_sub_wizard = ClientsValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_disclose_exec(self.disclose_exec)
        values_sub_wizard.set_id(self.id)
        values_sub_wizard.set_ext_id_client(self.ext_id_client)
        values_sub_wizard.set_name(self.name)
        assignment_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        assignment_tab.set_desk(self.desk)
        wizard = ClientsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(1)

        main_page.set_name(self.name)
        time.sleep(1)
        self.verify("New Client has been create", True, main_page.is_searched_client_found(self.name))
