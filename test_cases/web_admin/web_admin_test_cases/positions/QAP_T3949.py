import time
import string
import random

from test_framework.web_admin_core.pages.positions.wash_books.wash_books_page import WashBookPage
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_wizard import WashBookWizard
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_assignments_sub_waizard import WashBookAssignmentsSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3949(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.institution = self.data_set.get_institution("institution_1")
        self.id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client = self.data_set.get_client("client_1")
        self.client_id_source = self.data_set.get_client_id_source("client_id_source_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_washbook_page()
        time.sleep(2)

    def test_context(self):
        self.precondition()

        wash_book_main_menu = WashBookPage(self.web_driver_container)
        wash_book_main_menu.click_on_new_button()
        wash_book_wizard = WashBookWizard(self.web_driver_container)
        wash_book_wizard.set_id_at_values_tab(self.id)
        wash_book_wizard.set_ext_id_client_at_values_tab(self.ext_id_client)
        wash_book_wizard.set_client_at_values_tab(self.client)
        wash_book_wizard.set_client_id_source_at_values_tab(self.client_id_source)
        wash_book_wizard_assignment_tab = WashBookAssignmentsSubWizard(self.web_driver_container)
        wash_book_wizard_assignment_tab.set_institution(self.institution)
        expected_pdf_content = [f"ID: {self.id}",
                                f"Ext ID Client: {self.ext_id_client}",
                                "Client ID Source: BIC",
                                "Clearing Account Type: Institution",
                                f"Institution: {self.institution}"]
        self.verify(f"Is PDF contains {expected_pdf_content}", True,
                    wash_book_wizard.click_on_download_pdf_button_and_check_data(expected_pdf_content))

        wash_book_wizard.click_on_save_changes()
        wash_book_main_menu.set_id_filter(self.id)
        time.sleep(1)
        self.verify("WashBook Account is created and displayed on WashBook Accounts page.", True,
                    wash_book_main_menu.is_searched_entity_found(self.id))
