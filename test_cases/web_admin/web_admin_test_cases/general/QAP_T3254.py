import time

from test_framework.web_admin_core.pages.general.system_components.main_page import MainPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3254(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.preview = {"instance_id_1": "AQS", "short_name_1": "aqs", "long_name_1": "Admin and Query Servers",
                        "instance_id_2": "ALS", "short_name_2": "als", "long_name_2": "Alert Module"}
        self.active = ['true', 'false']
        self.version = str

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        self.version = login_page.get_version().split()[1][:11]
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_system_components_page()
        time.sleep(15)

    def test_context(self):

        self.precondition()

        main_page = MainPage(self.web_driver_container)
        main_page.set_instance_id(self.preview["instance_id_1"])
        main_page.set_short_name(self.preview["short_name_1"])
        main_page.set_long_name(self.preview["long_name_1"])
        main_page.set_version(self.version)
        main_page.set_active(self.active[0])

        self.verify("AQS component displayed at main page with active status", True,
                    main_page.is_active_status_displayed())

        main_page.set_instance_id(self.preview["instance_id_2"])
        main_page.set_short_name(self.preview["short_name_2"])
        main_page.set_long_name(self.preview["long_name_2"])
        main_page.set_version(self.version)
        main_page.set_active(self.active[1])

        time.sleep(1)
        self.verify("BS component displayed", True, main_page.is_searched_entity_found_by_name(
            self.preview["long_name_2"]))
        self.verify("Active status not displayed", False, main_page.is_active_status_displayed())
