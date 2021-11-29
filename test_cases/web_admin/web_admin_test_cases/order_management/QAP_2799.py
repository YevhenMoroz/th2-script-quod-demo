import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_conditions_sub_wizard import \
    OrderManagementRulesConditionsSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_default_result_sub_wizard import \
    OrderManagementRulesDefaultResultSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_page import \
    OrderManagementRulesPage
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_values_sub_wizard import \
    OrderManagementRulesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_wizard import \
    OrderManagementRulesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2799(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.condition_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.conditional_logic = " NOT IN "
        self.exec_policy = 'DMA'
        self.client = " LOAD "
        self.percentage = "100"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_order_management_rules_page()
        page = OrderManagementRulesPage(self.web_driver_container)
        values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
        conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
        default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
        wizard = OrderManagementRulesWizard(self.web_driver_container)

        page.click_on_new_button()
        time.sleep(2)
        conditions_sub_wizard.click_on_plus()
        time.sleep(2)
        conditions_sub_wizard.set_name(self.name)
        time.sleep(1)
        conditions_sub_wizard.set_qty_precision("100")
        time.sleep(1)
        conditions_sub_wizard.click_on_add_condition()
        time.sleep(1)
        conditions_sub_wizard.set_conditional_logic(self.conditional_logic)
        time.sleep(1)
        conditions_sub_wizard.set_right_side_list_at_conditional_logic(self.client)
        time.sleep(1)
        conditions_sub_wizard.click_on_plus_at_results_sub_wizard()
        time.sleep(2)
        conditions_sub_wizard.set_exec_policy(self.exec_policy)
        time.sleep(2)
        conditions_sub_wizard.set_percentage(self.percentage)
        time.sleep(2)
        conditions_sub_wizard.click_on_checkmark_at_results_sub_wizard()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = OrderManagementRulesPage(self.web_driver_container)
            conditions_sub_wizard = OrderManagementRulesConditionsSubWizard(self.web_driver_container)
            values_sub_wizard = OrderManagementRulesValuesSubWizard(self.web_driver_container)
            wizard = OrderManagementRulesWizard(self.web_driver_container)
            page = OrderManagementRulesPage(self.web_driver_container)
            default_result_sub_wizard = OrderManagementRulesDefaultResultSubWizard(self.web_driver_container)
            try:
                conditions_sub_wizard.click_on_checkmark()
                self.verify("Entity created correctly", True, True)





            except Exception:
                self.verify("Entity NOT created ", True, False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
