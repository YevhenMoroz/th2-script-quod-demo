import time

from selenium.common.exceptions import ElementNotInteractableException
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4010(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.desks = [self.data_set.get_desk("desk_1"), self.data_set.get_desk("desk_3")]

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
        self.precondition()
        try:
            assignments_tab.set_location("test")
        except ElementNotInteractableException as e:
            error_name = e.__class__.__name__
            self.verify("after select desks, location; zone; institution are disabled ",
                        "ElementNotInteractableException",
                        error_name)

        try:
            time.sleep(2)
            self.verify("after click on download PDF button", True,
                        users_wizard.click_download_pdf_entity_button_and_check_pdf(self.desks))
        except IndexError as e:
            print(e.__class__.__name__)
            self.verify("Download button is deactivated", True, False)