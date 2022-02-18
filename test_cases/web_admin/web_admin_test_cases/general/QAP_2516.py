import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2516(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.new_link = "https://support.quodfinancial.com/confluence/login.action?os_destination=%2Fdashboard.action&permissionViolation=true#all-udates"

    def test_context(self):

        try:
            main_page = CommonPage(self.web_driver_container)
            try:
                main_page.click_on_help_icon_at_login_page()
                self.verify("Help icon works", True, True)
            except Exception as e:
                self.verify("Help icon not works", True, e.__class__.__name__)

            try:
                time.sleep(2)
                self.verify("New link is open", True, main_page.is_link_of_help_icon_correct(self.new_link))
            except Exception as e:
                self.verify("Wrong new link", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
