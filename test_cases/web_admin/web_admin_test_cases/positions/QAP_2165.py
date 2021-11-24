import time
import traceback
from datetime import datetime

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.positions.wash_books.wash_books_page import WashBookPage
from test_cases.web_admin.web_admin_core.pages.positions.wash_books.wash_books_wizard import WashBookWizard
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2165(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        now = datetime.now()
        '''
        iteration_value this variable was created for concatenation id and ext_id_client values,
        because this values must be unique all time
        '''
        iteration_value = now.strftime("%d/%m/%Y %H:%M:%S")
        self.id = "test 2165: " + str(iteration_value)
        self.ext_id_client = "65: " + str(iteration_value)
        self.client = "CLIENT1"
        self.client_id_source = "BIC"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm03")
        login_page.set_password("adm03")
        login_page.click_login_button()
        login_page.check_is_login_successful()
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_washbook_page()
        time.sleep(2)
        wash_book_main_menu = WashBookPage(self.web_driver_container)
        wash_book_main_menu.click_on_new_button()
        wash_book_wizard = WashBookWizard(self.web_driver_container)
        time.sleep(1)
        wash_book_wizard.set_id_at_values_tab(self.id)
        time.sleep(1)
        wash_book_wizard.set_ext_id_client_at_values_tab(self.ext_id_client)
        time.sleep(2)
        wash_book_wizard.set_client_at_values_tab(self.client)
        time.sleep(2)
        wash_book_wizard.set_client_id_source_at_values_tab(self.client_id_source)
        time.sleep(2)
        wash_book_wizard.click_on_save_changes()
        time.sleep(1)
        wash_book_main_menu.set_id_filter(self.id)
        time.sleep(1)
        wash_book_main_menu.set_enabled_filter("true")
        time.sleep(2)
        wash_book_main_menu.click_on_more_actions()

    def test_context(self):
        try:
            self.precondition()
            wash_book_main_menu = WashBookPage(self.web_driver_container)
            expected_pdf_content = ["ID: {}".format(wash_book_main_menu.get_id_at_main_page()),
                                    "Ext ID Client: {}".format(wash_book_main_menu.get_ext_id_client_at_main_page()),
                                    "Client ID Source: BIC",
                                    "Clearing Account Type: Firm"]

            self.verify(f"Is PDF contains {expected_pdf_content}", True,
                        wash_book_main_menu.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
