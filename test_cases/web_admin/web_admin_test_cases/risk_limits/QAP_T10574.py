import random
import string
import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.wizards import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10574(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")
        self.instrument_type = "Equity"
        self.instrument = self.data_set.get_instrument("instrument_5")
        self.underlying_instrument = data_set.get_instrument("instrument_5")
        self.haircut_values = '10'
        self.removed_fields = ['PosValidity', 'Settlement Period', 'Holdings Ratio',
                               'Allow Securities on Negative Ledgers', 'Disallow for same Listing',
                               'Disallow for deliverable contracts']
        self.instrument_group = self.data_set.get_instrument_group("instrument_group_1")
        self.expected_error = "Incorrect or missing values"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_buying_power_page()

    def post_condition(self):
        main_page = MainPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        assignment_tab = AssignmentsTab(self.web_driver_container)
        security_values_tab = SecurityValuesTab(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new_button()
            values_tab.set_name(self.name)
            assignment_tab.set_institution(self.institution)
            security_values_tab.click_on_plus_in_table()
            security_values_tab.set_instrument_type(self.instrument_type)
            security_values_tab.set_instrument_group(self.instrument_group)
            security_values_tab.set_instrument(self.instrument)
            security_values_tab.set_underlying_listing(self.underlying_instrument)
            security_values_tab.click_on_save_checkmark_in_table()
            time.sleep(0.5)
            self.verify("Footer error appears", self.expected_error, wizard.get_footer_error_text())
            security_values_tab.set_haircut_value(self.haircut_values)
            security_values_tab.click_on_save_checkmark_in_table()
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            security_values_tab.click_on_edit_in_table()

            expected_result = [self.name, self.institution, self.haircut_values, self.instrument_type,
                               self.instrument_group, self.instrument, self.underlying_instrument]
            actual_result = [values_tab.get_name(), assignment_tab.get_institution(),
                             security_values_tab.get_haircut_value(), security_values_tab.get_instrument_type(),
                             security_values_tab.get_instrument_group(), security_values_tab.get_instrument(),
                             security_values_tab.get_underlying_listing()]
            self.verify("Saved data displayed correct", expected_result, actual_result)

            expected_result = [False for _ in range(len(self.removed_fields))]
            actual_result = [wizard.is_text_inside_wizard_found_by_patter(_) for _ in self.removed_fields]
            self.verify("Removed fields not disabled", expected_result, actual_result)
            wizard.click_on_save_changes()

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
