import time

from test_framework.web_admin_core.pages.general.system_commands.system_commands_page import SystemCommandsPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3921(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.system_commands = self.data_set.get_system_command("system_command_1")
        self.component_id = self.data_set.get_component_id("component_id_1")
        self.name = "test"
        self.value = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_system_commands_page()
        time.sleep(2)
        system_commands_page = SystemCommandsPage(self.web_driver_container)
        system_commands_page.set_system_commands(self.system_commands)
        system_commands_page.set_component_id(self.component_id)
        time.sleep(1)
        system_commands_page.click_on_plus()
        system_commands_page.set_name(self.name)
        system_commands_page.set_value(self.value)
        time.sleep(1)
        system_commands_page.click_on_checkmark()
        time.sleep(2)
        system_commands_page.click_on_send()
        time.sleep(30)

    def test_context(self):

        self.precondition()
        system_commands_page = SystemCommandsPage(self.web_driver_container)
        self.verify("Error message is displayed", True, system_commands_page.is_error_displayed())
