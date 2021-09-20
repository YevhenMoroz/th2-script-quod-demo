import time
import traceback

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_918(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.desks = ["Desk Market Marking FX", "Desk of Dealers 1"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_new_button()
        time.sleep(2)
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.click_on_desks()
        assignments_tab.set_desks(self.desks)

    def test_context(self):
        assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
        users_wizard = UsersWizard(self.web_driver_container)
        try:
            self.precondition()
            try:
                assignments_tab.set_location("test")
            except ElementNotInteractableException as e:
                error_name = e.__class__.__name__
                self.verify("after select desks, location; zone; institution are disabled ",
                            "ElementNotInteractableException",
                            error_name)

            try:
                self.verify("after click on download PDF button", True,
                            users_wizard.click_download_pdf_entity_button_and_check_pdf(self.desks))
            except IndexError as e:
                print(e.__class__.__name__)
                self.verify("Download button is deactivated", True, False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
