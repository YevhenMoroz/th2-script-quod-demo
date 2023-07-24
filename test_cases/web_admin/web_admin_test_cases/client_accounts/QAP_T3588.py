import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_page import ClientsPage
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_assignments_sub_wizard \
    import ClientsAssignmentsSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3588(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        self.precondition()

        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_clients_page()
        time.sleep(2)
        client_page = ClientsPage(self.web_driver_container)
        client_page.click_on_new()
        time.sleep(2)
        client_assignments_tab = ClientsAssignmentsSubWizard(self.web_driver_container)
        self.verify("The field User Manager is displayed", True,
                    client_assignments_tab.is_user_manager_field_displayed_and_has_correct_name())

        self.verify("The field Desk is displayed", True,
                    client_assignments_tab.is_desk_field_displayed_and_has_correct_name())
