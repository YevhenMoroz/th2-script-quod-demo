import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3855(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.link320 = 'http://10.0.22.38:6380/adm/qakharkiv320/#/auth/login'

    def test_context(self):

        try:
            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.login, self.password)
            time.sleep(2)
            common_page = CommonPage(self.web_driver_container)
            site1_cookies = common_page.get_browser_cookies()

            common_page.open_new_browser_tab_and_set_url(self.link320)
            time.sleep(2)
            login_page.login_to_web_admin(self.login, self.password)
            site2_cookies = common_page.get_browser_cookies()

            self.verify("Is cookies equal?", False, site1_cookies == site2_cookies)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
