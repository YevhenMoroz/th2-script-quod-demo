import random
import sys
import time
import traceback
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3809(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.user = ''
        self.desk = ''
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
        self.account = random.choice(wizard.get_all_account_from_drop_menu())
        wizard.set_account(self.account)
        wizard.set_institution(self.institution)
        wizard.click_on_save_changes()
        page.set_name_at_filter(self.name)
        time.sleep(1)

    def post_condition(self):
        wizard = WashBookRulesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        page = WashBookRulesPage(self.web_driver_container)
        page.set_name_at_filter(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_delete_and_confirmation(True)

    def test_context(self):
        try:
            self.precondition()

            page = WashBookRulesPage(self.web_driver_container)
            page.click_on_more_actions()
            page.click_on_edit_at_more_actions()
            wizard = WashBookRulesWizard(self.web_driver_container)
            self.desk = random.choice(wizard.get_all_desk_from_drop_menu())
            wizard.set_desk(self.desk)
            self.user = random.choice(wizard.get_all_users_from_drop_menu())
            wizard.set_user(self.user)
            wizard.click_on_save_changes()
            page.set_name_at_filter(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit_at_more_actions()

            self.verify("WashBookRules contains saved Desk and User", [self.user, self.desk],
                        [wizard.get_user(), wizard.get_desk()])

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
