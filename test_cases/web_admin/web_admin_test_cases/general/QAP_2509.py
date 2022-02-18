import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2509(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "Qwerty123!"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        main_page = CommonPage(self.web_driver_container)
        try:
            self.precondition()
            try:
                main_page.click_on_send_feedback_button()
                time.sleep(2)
                self.verify("[SEND] button is disable", False, main_page.is_send_button_at_feedback_area_disabled_enabled())

                main_page.set_text_to_feedback_text_area("test")
                time.sleep(1)
                self.verify("[SEND]  button is enable after enter some text", True, main_page.is_send_button_at_feedback_area_disabled_enabled())
            except Exception as e:
                self.verify("Send button does not work", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
