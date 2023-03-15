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


class QAP_T10584(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")
        self.expected_error = 'Incorrect or missing values'
        self.instrument_type = ['Option', 'Equity']
        self.instrument = ['USD/TWD', 'BUN-CITQ']
        self.underlying_instrument = ['EUR/KES', 'GBP/BRL']
        self.initial_margin = '5'
        self.margin_method = ['VenueSpecified', 'CustomAmount']

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
        risk_margin_tab = RiskMarginTab(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new_button()
            values_tab.set_name(self.name)
            assignment_tab.set_institution(self.institution)
            risk_margin_tab.click_on_plus_in_table()
            risk_margin_tab.set_instrument_type(self.instrument_type[0])
            risk_margin_tab.set_instrument(self.instrument[0])
            risk_margin_tab.set_underlying_instrument(self.underlying_instrument[0])
            risk_margin_tab.click_on_save_checkmark_in_table()
            time.sleep(0.5)
            self.verify("Footer error appears", self.expected_error, wizard.get_footer_error_text())

            risk_margin_tab.set_initial_margin(self.initial_margin)
            risk_margin_tab.click_on_save_checkmark_in_table()
            time.sleep(0.5)
            self.verify("Footer error appears", self.expected_error, wizard.get_footer_error_text())

            risk_margin_tab.set_margin_method(self.margin_method[0])
            time.sleep(0.5)
            actual_result = [risk_margin_tab.get_initial_margin()]
            if "Initial Margin" in actual_result:
                actual_result = list(map(lambda x: x.replace('Initial Margin', ''), actual_result))
            self.verify("Initial Margin field become blank", [''], actual_result)
            risk_margin_tab.click_on_save_checkmark_in_table()
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            risk_margin_tab.click_on_edit_in_table()
            time.sleep(0.5)
            expected_result = [self.margin_method[0], "", self.instrument_type[0], self.instrument[0],
                               self.underlying_instrument[0]]
            actual_result = [risk_margin_tab.get_margin_method(), risk_margin_tab.get_initial_margin(),
                             risk_margin_tab.get_instrument_type(), risk_margin_tab.get_instrument(),
                             risk_margin_tab.get_underlying_instrument()]
            if "Initial Margin" in actual_result:
                actual_result = list(map(lambda x: x.replace('Initial Margin', ''), actual_result))
            self.verify("Risk Margin entity saved correct", expected_result, actual_result)

            risk_margin_tab.set_margin_method(self.margin_method[1])
            risk_margin_tab.click_on_save_checkmark_in_table()
            time.sleep(0.5)
            self.verify("Footer error appears", self.expected_error, wizard.get_footer_error_text())

            risk_margin_tab.set_initial_margin(self.initial_margin)
            risk_margin_tab.click_on_save_checkmark_in_table()
            risk_margin_tab.click_on_plus_in_table()
            risk_margin_tab.set_margin_method(self.margin_method[0])
            risk_margin_tab.set_instrument_type(self.instrument_type[1])
            risk_margin_tab.click_on_save_checkmark_in_table()
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            risk_margin_tab.set_instrument_type_filter(self.instrument_type[0])
            time.sleep(0.5)
            risk_margin_tab.click_on_edit_in_table()
            time.sleep(0.5)
            expected_result_1 = [self.margin_method[1], self.initial_margin, self.instrument_type[0], self.instrument[0],
                                 self.underlying_instrument[0]]
            actual_result_1 = [risk_margin_tab.get_margin_method(), risk_margin_tab.get_initial_margin(),
                               risk_margin_tab.get_instrument_type(), risk_margin_tab.get_instrument(),
                               risk_margin_tab.get_underlying_instrument()]
            print(expected_result_1)
            print(actual_result_1)
            self.verify("Table entity 1 saved correct",
                        expected_result_1,
                        actual_result_1)
            risk_margin_tab.click_on_cancel_in_table()

            risk_margin_tab.set_instrument_type_filter(self.instrument_type[1])
            time.sleep(0.5)
            risk_margin_tab.click_on_edit_in_table()
            time.sleep(0.5)
            expected_result_2 = [self.margin_method[0], self.instrument_type[1]]
            actual_result_2 = [risk_margin_tab.get_margin_method(), risk_margin_tab.get_instrument_type()]

            self.verify("Table entity 2 saved correct", expected_result_2, actual_result_2)
            risk_margin_tab.click_on_cancel_in_table()
            wizard.click_on_close()

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
