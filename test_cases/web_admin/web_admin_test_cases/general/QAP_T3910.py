import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3910(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_user("user_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        main_page = CommonPage(self.web_driver_container)

        self.precondition()
        try:
            main_page.click_on_send_feedback_button()
            time.sleep(2)
            self.verify("[SEND] button is disable", False,
                        main_page.is_send_button_at_feedback_area_disabled_enabled())

            main_page.set_text_to_feedback_text_area("test")
            time.sleep(1)
            self.verify("[SEND]  button is enable after enter some text", True,
                        main_page.is_send_button_at_feedback_area_disabled_enabled())
        except Exception as e:
            self.verify("Send button does not work", True, e.__class__.__name__)
