import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3517(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        main_page = CommonPage(self.web_driver_container)
        main_page.click_on_send_feedback_button()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            main_page = CommonPage(self.web_driver_container)
            try:
                main_page.click_on_application_information_at_send_feedback()
                time.sleep(2)
                self.verify("Addition information opened and contains correct data",
                            self.login, main_page.get_user_id_at_send_feedback())
            except Exception as e:
                self.verify("Addition information not opened or incorrect", True, e.__class__.__name__)

            try:
                main_page.click_on_arrow_back_button_at_send_feedback()
                time.sleep(2)
                self.verify("[←] Back button work correctly", True,
                            main_page.is_send_feedback_field_displayed())
            except Exception as e:
                self.verify("[←] Back button does not work", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
