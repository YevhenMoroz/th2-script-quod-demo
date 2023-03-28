import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3412(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_14")
        self.password = self.data_set.get_password("password_14")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")
        self.account = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_washbook_rules_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            page = WashBookRulesPage(self.web_driver_container)
            page.click_on_new_button()
            time.sleep(2)
            wizard = WashBookRulesWizard(self.web_driver_container)
            wizard.set_name(self.name)
            self.account = random.choice(wizard.get_all_account_from_drop_menu())
            wizard.set_account(self.account)
            available_institutions = wizard.get_all_institutions_from_drop_menu()
            actual_result = bool
            for i in available_institutions:
                if i != self.institution:
                    actual_result = False
                    break
                else:
                    actual_result = True
            self.verify(f"Only {self.institution} available to choose", True, actual_result)

            wizard.set_institution(self.institution)
            time.sleep(1)
            wizard.click_on_save_changes()
            time.sleep(2)
            page = WashBookRulesPage(self.web_driver_container)
            page.set_name_at_filter(self.name)
            time.sleep(1)
            self.verify("New WashBookRules has been create", True, page.is_searched_entity_found(self.name))

            page.click_on_more_actions()
            time.sleep(1)
            page.click_on_edit_at_more_actions()
            time.sleep(2)
            new_account = random.choice(wizard.get_all_account_from_drop_menu())
            wizard.set_account(new_account)
            wizard.click_on_save_changes()
            time.sleep(2)
            page.set_name_at_filter(self.name)
            time.sleep(1)
            self.verify("Current user can modify WashBookRules entity", True, page.is_searched_entity_found(self.name))

            page.click_on_more_actions()
            time.sleep(1)
            page.click_on_delete_and_confirmation(True)
            time.sleep(1)
            common_act = CommonPage(self.web_driver_container)
            common_act.refresh_page(True)
            time.sleep(3)
            page.set_name_at_filter(self.name)
            time.sleep(1)
            self.verify("Entity has been delete", False, page.is_searched_entity_found(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
