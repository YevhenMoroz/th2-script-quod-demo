import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3948(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_type = self.data_set.get_instr_type("instr_type_9")
        self.execution_policy = self.data_set.get_exec_policy("exec_policy_1")
        self.client = self.data_set.get_client("client_1")
        self.user = self.data_set.get_user("user_11")
        self.desk = self.data_set.get_desk("desk_1")
        self.institution = self.data_set.get_institution("institution_1")
        self.account = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_washbook_rules_page()
        page = WashBookRulesPage(self.web_driver_container)
        page.click_on_new_button()
        wizard = WashBookRulesWizard(self.web_driver_container)
        wizard.set_name(self.name)
        wizard.set_instr_type(self.instr_type)
        wizard.set_execution_policy(self.execution_policy)
        self.account = random.choice(wizard.get_all_account_from_drop_menu())
        wizard.set_account(self.account)
        wizard.set_client(self.client)
        wizard.set_user(self.user)
        wizard.set_desk(self.desk)
        wizard.set_institution(self.institution)

    def test_context(self):
        try:
            self.precondition()
            wizard = WashBookRulesWizard(self.web_driver_container)
            page = WashBookRulesPage(self.web_driver_container)

            expected_content = [self.name, self.client, self.instr_type, self.execution_policy, self.account,
                                self.user, self.desk]
            self.verify("Is pdf contains values ", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_content))
            wizard.click_on_save_changes()
            page.set_name_at_filter(self.name)
            time.sleep(1)
            headers = ["Name", "Client", "Instr Type", "Execution Policy", "WashBook Account", "User", "Desk"]
            actual_content = [page.get_name(), page.get_client(), page.get_instr_type(), page.get_execution_policy(),
                              page.get_wash_book_account(), page.get_user(),
                              page.get_desk()]
            self.verify_arrays_of_data_objects("Is data saved correctly in main page", headers, expected_content,
                                               actual_content)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
