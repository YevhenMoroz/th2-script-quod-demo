import sys
import traceback
import time

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7866(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.info_message_text = 'Feedback sent'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        try:
            self.precondition()

            common_act = CommonPage(self.web_driver_container)
            common_act.click_on_send_feedback_button()
            common_act.set_text_to_feedback_text_area("QAP-T7866 test")
            common_act.click_on_send_button_at_feedback_area()

            time.sleep(2)
            self.verify("Info popup about successful sending appears", True, common_act.is_info_message_displayed())
            self.verify("Popup contains text 'Feedback sent'", self.info_message_text, common_act.get_info_pop_up_text())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
