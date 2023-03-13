import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.wizards import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3335(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = 'QUOD FINANCIAL'
        self.global_margin = '1'
        self.instrument_type = 'Bond'
        self.instrument_group = 'TC Danish'
        self.underling_listing = 'AMANAT'
        self.haircut_value = '2'
        self.margin_method = 'CustomAmount'
        self.initial_margin = '3'
        self.maintenance_margin = '4'
        self.instrument_type_risk_margin = 'Equity'
        self.instrument = 'AMANAT'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_buying_power_page()
            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name)
            assignments_tab = AssignmentsTab(self.web_driver_container)
            assignments_tab.set_institution(self.institution)
            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            self.verify("New entity has been create", True, main_page.is_searched_entity_found_by_name(self.name))
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            values_tab.set_name(self.new_name)
            values_tab.set_description(self.description)

            cash_values_tab = CashValuesTab(self.web_driver_container)
            cash_values_tab.set_cash_checkbox()
            cash_values_tab.set_temporary_cash_checkbox()

            security_values = SecurityValuesTab(self.web_driver_container)
            security_values.set_trade_on_margin_checkbox()
            security_values.set_global_margin(self.global_margin)
            security_values.click_on_plus_in_table()
            security_values.set_instrument_type(self.instrument_type)
            security_values.set_instrument_group(self.instrument_group)
            security_values.set_underlying_listing(self.underling_listing)
            security_values.set_haircut_value(self.haircut_value)
            security_values.click_on_save_checkmark_in_table()

            risk_margin = RiskMarginTab(self.web_driver_container)
            risk_margin.click_on_plus_in_table()
            risk_margin.set_margin_method(self.margin_method)
            risk_margin.set_initial_margin(self.initial_margin)
            #risk_margin.set_maintenance_margin(self.maintenance_margin)
            risk_margin.set_instrument_type(self.instrument_type_risk_margin)
            #risk_margin.set_instrument_group(self.instrument_group)
            risk_margin.set_instrument(self.instrument)
            risk_margin.set_underlying_instrument(self.underling_listing)
            risk_margin.click_on_save_checkmark_in_table()

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.new_name)
            time.sleep(1)
            self.verify("New entity has been edit", True, main_page.is_searched_entity_found_by_name(self.new_name))
            main_page.click_on_more_actions()
            main_page.click_on_clone()

            expected_result = [self.description, self.institution, "Cash: False", "Temporary Cash: True",
                               "Trade on Margin: True", self.global_margin, self.instrument_type, self.instrument_group,
                               self.underling_listing, self.haircut_value, self.margin_method, self.initial_margin,
                               self.maintenance_margin, self.maintenance_margin, self.instrument_type,
                               self.instrument_group, self.instrument, self.underling_listing]

            security_values.click_on_edit_in_table()
            risk_margin.click_on_edit_in_table()
            actual_result = [values_tab.get_description(), assignments_tab.get_institution(),
                             f"Cash: {cash_values_tab.is_cash_checkbox_selected()}",
                             f"Temporary Cash: {cash_values_tab.is_temporary_cash_checkbox_selected()}",
                             f"Trade on Margin: {security_values.is_trade_on_margin_checkbox_selected()}",
                             security_values.get_global_margin(), security_values.get_instrument_type(),
                             security_values.get_instrument_group(), security_values.get_underlying_listing(),
                             security_values.get_haircut_value(), risk_margin.get_margin_method(),
                             risk_margin.get_initial_margin(), risk_margin.get_maintenance_margin(),
                             risk_margin.get_instrument_type(), risk_margin.get_instrument_group(),
                             risk_margin.get_instrument(), risk_margin.get_underlying_instrument()]

            self.verify("Not required fields autofill", expected_result, actual_result)

            values_tab.set_name(self.name)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_delete(True)
            main_page.set_name_filter(self.name)
            time.sleep(1)
            self.verify("Entity has been delete", False, main_page.is_searched_entity_found_by_name(self.name))
            main_page.set_name_filter(self.new_name)
            time.sleep(1)
            self.verify("Download PDF button works", True,
                        main_page.click_download_pdf_entity_button_and_check_pdf(self.new_name))
            main_page.click_on_more_actions()
            main_page.click_on_pin_row()
            time.sleep(1)
            self.verify("Entity pinned", True, main_page.is_entity_pinned(self.new_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
