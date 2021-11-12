import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2616(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            common_page = CommonPage(self.web_driver_container)
            try:
                self.verify("Is help icon displayed", True, common_page.is_help_icon_displayed())
                self.verify("Is send feedback icon displayed", True, common_page.is_send_feedback_icon_displayed())
                self.verify("Is user name icon displayed", True, common_page.is_user_name_icon_displayed())
                self.verify("Is user icon displayed", True, common_page.is_user_icon_displayed())

            except Exception as e:
                self.verify("Some of icon not active !", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
