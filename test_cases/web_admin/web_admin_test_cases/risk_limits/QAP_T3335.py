import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.wizards import ValuesTab, CashValuesTab, \
    SecurityValuesTab, MainWizard
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
        self.reference_value = 'LastTradedPrice'
        self.holding_ratio = '10'
        self.settlement_period = 'TPlus4'
        self.position_validity = 'TPlus5'
        self.margin_method = 'CustomPercentage'
        self.custom_percentage = '74'

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
            cash_values_tab.set_cash_loan_checkbox()
            cash_values_tab.set_collateral_checkbox()
            cash_values_tab.set_allow_collateral_on_negative_ledger_checkbox()

            security_values = SecurityValuesTab(self.web_driver_container)
            security_values.set_include_securities_checkbox()
            security_values.set_reference_value(self.reference_value)
            security_values.set_holdings_ratio(self.holding_ratio)
            security_values.click_on_plus_in_table()
            security_values.set_settlement_period(self.settlement_period)
            security_values.set_position_validity(self.position_validity)
            security_values.set_margin_method(self.margin_method)
            security_values.set_custom_percentage(self.custom_percentage)
            security_values.set_allow_securities_on_negative_ledgers_checkbox()
            security_values.set_disallow_for_same_listing_checkbox()
            security_values.set_disallow_for_deliverable_contracts_checkbox()

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.new_name)
            time.sleep(1)
            self.verify("New entity has been edit", True, main_page.is_searched_entity_found_by_name(self.new_name))
            main_page.click_on_more_actions()
            main_page.click_on_clone()

            expected_result = [self.description, "Cash: True", "Temporary Cash: True", "Cash Loan: True",
                               "Collateral: True", "Allow Collateral on Negative Ledger: True",
                               "Include Securities: True", self.reference_value, self.holding_ratio,
                               self.settlement_period, self.position_validity, self.margin_method,
                               self.custom_percentage, "Allow Securities on Negative Ledgers: True",
                               "Disallow for same Listing: True", "Disallow for deliverable contracts: True"]
            security_values.click_on_edit_in_table()
            actual_result = [values_tab.get_description(), f"Cash: {cash_values_tab.is_cash_checkbox_selected()}",
                             f"Temporary Cash: {cash_values_tab.is_temporary_cash_checkbox_selected()}",
                             f"Cash Loan: {cash_values_tab.is_cash_loan_checkbox_selected()}",
                             f"Collateral: {cash_values_tab.is_collateral_checkbox_selected()}",
                             f"Allow Collateral on Negative Ledger: {cash_values_tab.is_allow_collateral_on_negative_ledger_checkbox_selected()}",
                             f"Include Securities: {security_values.is_include_securities_checkbox_selected()}",
                             security_values.get_reference_value(), security_values.get_holding_ratio(),
                             security_values.get_settlement_period(), security_values.get_position_validity(),
                             security_values.get_margin_method(), security_values.get_custom_percentage(),
                             f"Allow Securities on Negative Ledgers: {security_values.is_allow_securities_on_negative_ledgers_checkbox_selected()}",
                             f"Disallow for same Listing: {security_values.is_disallow_for_same_listing_checkbox_selected()}",
                             f"Disallow for deliverable contracts: {security_values.is_disallow_for_deliverable_contracts_checkbox_selected()}"]

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
