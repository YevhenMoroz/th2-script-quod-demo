import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3947(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.execution_policy = self.data_set.get_exec_policy("exec_policy_2")
        self.institution = self.data_set.get_institution("institution_1")
        self.account = ''

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
        self.account = random.choice(wizard.get_all_account_from_drop_menu())
        wizard.set_account(self.account)
        time.sleep(1)
        wizard.set_institution(self.institution)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        self.precondition()

        page = WashBookRulesPage(self.web_driver_container)
        page.set_name_at_filter(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        expected_pdf_content = [self.name, self.instr_type, self.execution_policy,
                                self.account]
        self.verify("Is pdf contains values ", True,
                    page.click_download_pdf_entity_button_and_check_pdf(expected_pdf_content))
