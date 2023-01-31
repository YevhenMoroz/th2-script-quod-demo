import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_page import WashBookPage
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_wizard import WashBookWizard
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_assignments_sub_waizard \
    import WashBookAssignmentsSubWizard

from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_page import WashBookRulesPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_wizard import WashBookRulesWizard

from test_framework.web_admin_core.pages.site.institution.institutions_wizard \
    import InstitutionsWizard
from test_framework.web_admin_core.pages.site.institution.institution_values_sub_wizard \
    import InstitutionsValuesSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3404(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.institution = self.data_set.get_institution("institution_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_washbook_page()

            wash_book_main_page = WashBookPage(self.web_driver_container)
            wash_book_main_page.click_on_new_button()

            assignment_tab = WashBookAssignmentsSubWizard(self.web_driver_container)
            assignment_tab.set_institution(self.institution)
            assignment_tab.click_at_institution_link_by_name(self.institution)

            wizard = WashBookWizard(self.web_driver_container)
            wizard.click_on_no_button()

            institution_values_tab = InstitutionsValuesSubWizard(self.web_driver_container)

            self.verify("The system redirected the user to the settings of the selected Institution.",
                        self.institution, institution_values_tab.get_institution_name())

            institution_wizard = InstitutionsWizard(self.web_driver_container)
            institution_wizard.click_on_close()
            if institution_wizard.is_leave_page_confirmation_pop_up_displayed():
                institution_wizard.click_on_ok_button()

            side_menu.open_washbook_rules_page()
            wash_book_rules_page = WashBookRulesPage(self.web_driver_container)
            wash_book_rules_page.click_on_new_button()
            wizard = WashBookRulesWizard(self.web_driver_container)
            wizard.set_institution(self.institution)
            wizard.click_at_institution_link_by_name(self.institution)
            wizard.click_on_no_button()

            institution_values_tab = InstitutionsValuesSubWizard(self.web_driver_container)

            self.verify("The system redirected the user to the settings of the selected Institution.",
                        self.institution, institution_values_tab.get_institution_name())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
