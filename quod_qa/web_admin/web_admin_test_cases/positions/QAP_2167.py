import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from quod_qa.web_admin.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2167(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = "Bond"
        self.execution_policy = "DMA"
        self.account = "TEST"
        self.client = "CLIENT1"
        self.user = "adm01"
        self.desk = "DESK A"
        self.institution = "QUOD FINANCIAL"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_washbook_rules_page()
        page = WashBookRulesPage(self.web_driver_container)
        page.click_on_new_button()
        time.sleep(1)
        wizard = WashBookRulesWizard(self.web_driver_container)
        wizard.set_name(self.name)
        time.sleep(1)
        wizard.set_instr_type(self.instr_type)
        time.sleep(1)
        wizard.set_execution_policy(self.execution_policy)
        time.sleep(1)
        wizard.set_account(self.account)
        time.sleep(1)
        wizard.set_client(self.client)
        time.sleep(1)
        wizard.set_user(self.user)
        time.sleep(1)
        wizard.set_desk(self.desk)
        time.sleep(1)
        wizard.set_institution(self.institution)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = WashBookRulesPage(self.web_driver_container)
            page.set_name_at_filter(self.name)
            time.sleep(2)
            page.click_on_more_actions()
            expected_pdf_content = [self.name, self.client, self.instr_type, self.execution_policy, self.account,
                                    self.user, self.desk]
            self.verify("Is pdf contains values ", True,
                        page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
