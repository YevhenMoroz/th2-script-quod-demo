import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3918(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.new_link = "https://support.quodfinancial.com/confluence"
        self.opened_page = "#all-udates#ordermanagement-ordermgmtrules"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):

        self.precondition()
        main_page = CommonPage(self.web_driver_container)
        try:
            main_page.click_on_help_icon()
            self.verify("Help icon works", True, True)
        except Exception as e:
            self.verify("Help icon not works", True, e.__class__.__name__)

        try:
            main_page.switch_to_browser_tab_or_window(1)
            get_url = main_page.get_current_page_url()
            self.verify("New link is open", True, self.new_link and self.opened_page in get_url)
        except Exception as e:
            self.verify("Wrong new link", True, e.__class__.__name__)
