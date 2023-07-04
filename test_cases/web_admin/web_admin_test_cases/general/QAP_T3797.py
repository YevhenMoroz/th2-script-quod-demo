import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3797(CommonTestCase):

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
        main_page = CommonPage(self.web_driver_container)
        main_page.click_on_user_icon()
        time.sleep(2)
        main_page.click_on_about()
        time.sleep(1)
        version_from_copy_version_button = main_page.extract_version_from_copy_version()
        admin_version = main_page.extract_admin_version()
        self.verify("Is version compared", True, version_from_copy_version_button in admin_version)
