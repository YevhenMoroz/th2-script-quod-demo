import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.general.system_components.main_page import MainPage
from test_framework.web_admin_core.pages.general.system_components.wizard import Wizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3253(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.instance_id = 'AQS'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_system_components_page()
        time.sleep(2)

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        wizard = Wizard(self.web_driver_container)

        try:
            self.precondition()

            self.verify("The [Download CVS] button is displayed and after clicking on the button, "
                        "the file is downloaded",
                        True, len(main_page.click_on_download_csv_button_and_get_content()[0]['Version']) > 2)

            main_page.click_on_full_screen_button()
            time.sleep(1)
            self.verify("The [Full Screen/Non-Full Screen] button is displayed and after click on the button,"
                        " the page become full screen",
                        False, main_page.is_site_header_displayed())

            main_page.click_on_refresh_page_button()
            time.sleep(1)
            self.verify("The [Refresh Values] button is displayed and clickable", True, True)

            self.verify("The [NEW] button is not displayed", False, main_page.is_new_button_displayed())

            main_page.set_instance_id(self.instance_id)
            time.sleep(1)
            main_page.click_on_more_actions()
            time.sleep(1)
            self.verify("The [Clone] button is not displayed", False, main_page.is_clone_button_displayed())
            self.verify("The [Delete] button is not displayed", False, main_page.is_delete_button_displayed())
            self.verify("The [Download PDF] button is not displayed", False, main_page.is_download_pdf_button_displayed())

            main_page.click_on_pin_row()
            time.sleep(1)
            self.verify("Entity has been pinned", True, main_page.is_entity_pinned(self.instance_id))
            main_page.click_on_more_actions()
            main_page.click_on_pin_row()
            time.sleep(1)
            self.verify("Entity has been unpinned", False, main_page.is_entity_pinned(self.instance_id))

            main_page.click_on_more_actions()
            main_page.click_on_edit()
            time.sleep(1)
            self.verify("The wizard page is opened", True, wizard.is_wizard_open())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
