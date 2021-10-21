import time
import traceback

from selenium.common.exceptions import TimeoutException

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.general.admin_command.admin_command_page import AdminCommandPage
from quod_qa.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.general.settings.settings_page import SettingsPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2450(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.admin_command = "ChangeLogLevel"
        self.component_id = "SATS"
        self.name = "test"
        self.value = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_admin_command_page()
        time.sleep(2)
        admin_command_page = AdminCommandPage(self.web_driver_container)
        admin_command_page.set_admin_command(self.admin_command)
        admin_command_page.set_component_id(self.component_id)
        time.sleep(1)
        admin_command_page.click_on_plus()
        admin_command_page.set_name(self.name)
        admin_command_page.set_value(self.value)
        time.sleep(1)
        admin_command_page.click_on_checkmark()
        time.sleep(2)
        admin_command_page.click_on_send()
        time.sleep(7)

    def test_context(self):

        try:
            self.precondition()
            admin_command_page = AdminCommandPage(self.web_driver_container)
            self.verify("That row not exist", True, admin_command_page.is_error_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
